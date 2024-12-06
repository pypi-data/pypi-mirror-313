#!/usr/bin/python
#
# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING

from six.moves import configparser
import io
import os
import pwd
import shutil
import signal
import six
import random
from string import Template
import subprocess

from .control import TC


WRAP_HOSTNAME = 'idp.ipsilon.dev'
TESTREALM = 'IPSILON.DEV'
TESTDOMAIN = 'ipsilon.dev'
KDC_DBNAME = 'db.file'
KDC_STASH = 'stash.file'
KDC_PASSWORD = 'ipsilon'
KRB5_CONF_TEMPLATE = '''
[libdefaults]
  default_realm = ${TESTREALM}
  dns_lookup_realm = false
  dns_lookup_kdc = false
  rdns = false
  ticket_lifetime = 24h
  forwardable = yes
  default_ccache_name = FILE://${TESTDIR}/ccaches/krb5_ccache_XXXXXX
  udp_preference_limit = 0

[realms]
  ${TESTREALM} = {
    kdc =${WRAP_HOSTNAME}:8888
  }

[domain_realm]
  .${TESTDOMAIN} = ${TESTREALM}
  ${TESTDOMAIN} = ${TESTREALM}

[dbmodules]
  ${TESTREALM} = {
    database_name = ${KDCDIR}/${KDC_DBNAME}
  }
'''

KDC_CONF_TEMPLATE = '''
[kdcdefaults]
 kdc_ports = 8888
 kdc_tcp_ports = 8888
 restrict_anonymous_to_tgt = true

[realms]
 ${TESTREALM} = {
  master_key_type = aes256-cts
  max_life = 7d
  max_renewable_life = 14d
  acl_file = ${KDCDIR}/kadm5.acl
  dict_file = /usr/share/dict/words
  default_principal_flags = +preauth
  admin_keytab = ${TESTREALM}/kadm5.keytab
  key_stash_file = ${KDCDIR}/${KDC_STASH}
 }
[logging]
  kdc = FILE:${KDCLOG}
'''

USER_KTNAME = "user.keytab"
HTTP_KTNAME = "http.keytab"
KEY_TYPE = "aes256-cts-hmac-sha384-192:normal"


class IpsilonTestBase(object):

    def __init__(self, name, execname, allow_wrappers=True):
        self.name = name
        self.execname = execname
        self.py3 = False
        self.rootdir = os.getcwd()
        self.testdir = None
        self.testuser = pwd.getpwuid(os.getuid())[0]
        self.processes = []
        self.allow_wrappers = allow_wrappers
        self.current_setup_step = None
        self.print_cases = False
        self.stdout = None
        self.stderr = None

    def set_py3(self, use_py3):
        self.py3 = use_py3

    @property
    def pycmd(self):
        return 'python3' if self.py3 else 'python'

    def platform_supported(self):
        """This return whether the current platform supports this test.

        This is used for example with specific modules or features that are not
        supported on all platforms due to dependency availability.

        If the platform is supported, it returns None.
        Otherwise it returns a string indicating why the platform does not
        support the current test.
        """
        # Every test defaults to being available on every platform
        return None

    def force_remove(self, op, name, info):
        os.chmod(name, 0o700)
        os.remove(name)

    def setup_base(self, path, test):
        self.testdir = os.path.join(path, test.name)
        if os.path.exists(self.testdir):
            shutil.rmtree(self.testdir, onerror=self.force_remove)
        os.makedirs(self.testdir)
        shutil.copytree(os.path.join(self.rootdir, 'templates'),
                        os.path.join(self.testdir, 'templates'))
        os.mkdir(os.path.join(self.testdir, 'etc'))
        os.mkdir(os.path.join(self.testdir, 'lib'))
        os.mkdir(os.path.join(self.testdir, 'lib', test.name))
        os.mkdir(os.path.join(self.testdir, 'log'))
        os.mkdir(os.path.join(self.testdir, 'cache'))
        self.setup_ca()

    def setup_ca(self):
        # Prepare the cert stuff for this run
        os.mkdir(os.path.join(self.testdir, 'certs'))
        cmd = ['openssl', 'req', '-newkey', 'rsa:2048', '-days', '10',
               '-x509', '-nodes', '-subj', '/CN=Ipsilon Test CA',
               '-keyout', os.path.join(self.testdir, 'certs', 'root.key.pem'),
               '-out', os.path.join(self.testdir, 'certs', 'root.cert.pem')]
        subprocess.check_call(cmd,
                              stdout=self.stdout, stderr=self.stderr)
        open(os.path.join(self.testdir, 'certs', 'db'), 'w').close()

        with open(os.path.join(self.testdir, 'certs', 'serial'), 'w') as ser:
            ser.write('000b')

        with open(os.path.join(self.testdir, 'certs',
                               'openssl.conf'), 'w') as conf:
            conf.write("""[ ca ]
default_ca = myca
[ myca ]
database = %(certdir)s/db
serial = %(certdir)s/serial
x509_extensions = myca_extensions
policy = myca_policy
[ myca_policy ]
commonName = supplied
[ alt_names ]
DNS.1 = ${ENV::ADDR}
IP.1 = ${ENV::IPADDR}
[ myca_extensions ]
subjectKeyIdentifier = hash
subjectAltName = @alt_names
basicConstraints = CA:false""" % {'certdir': os.path.join(self.testdir,
                                                          'certs')})

    def generate_profile(self, global_opts, args_opts, name, addr, port,
                         nameid='unspecified'):
        args_opts['port'] = port

        newconf = configparser.RawConfigParser()
        newconf.add_section('globals')
        for k in global_opts:
            newconf.set('globals', k, global_opts[k])
        newconf.add_section('arguments')
        for k in args_opts:
            newconf.set('arguments', k, args_opts[k])

        if six.PY2:
            profile = io.BytesIO()
        elif six.PY3:
            profile = io.StringIO()
        newconf.write(profile)

        t = Template(profile.getvalue())
        text = t.substitute({'NAME': name, 'ADDRESS': addr, 'PORT': port,
                             'TESTDIR': self.testdir,
                             'ROOTDIR': self.rootdir,
                             'NAMEID': nameid,
                             'HTTP_KTNAME': HTTP_KTNAME,
                             'TEST_USER': self.testuser})

        filename = os.path.join(self.testdir, '%s_profile.cfg' % name)
        with open(filename, 'w') as f:
            f.write(text)

        return filename

    def setup_http(self, name, addr, port):
        httpdir = os.path.join(self.testdir, name)
        os.mkdir(httpdir)
        os.mkdir(os.path.join(httpdir, 'conf.d'))
        os.mkdir(os.path.join(httpdir, 'html'))
        os.mkdir(os.path.join(httpdir, 'logs'))
        os.symlink('/etc/httpd/modules', os.path.join(httpdir, 'modules'))

        with open(os.path.join(self.rootdir, 'tests/httpd.conf')) as f:
            t = Template(f.read())
            text = t.substitute({'HTTPROOT': httpdir,
                                 'HTTPADDR': addr,
                                 'HTTPPORT': port,
                                 'NAME': name,
                                 'CERTROOT': os.path.join(self.testdir,
                                                          'certs'),
                                 'PYTHON3': '_python3' if self.py3 else ''})
        filename = os.path.join(httpdir, 'httpd.conf')
        with open(filename, 'w+') as f:
            f.write(text)

        certpath = os.path.join(self.testdir, 'certs', '%s.pem' % name)
        keypath = os.path.join(self.testdir, 'certs', '%s.key' % name)
        self.generate_cert(name, addr, certpath, keypath)

        return filename

    def generate_cert(self, name, addr, certpath, keypath):
        # Generate certs for this setup
        cmd = ['openssl', 'req', '-newkey', 'rsa:2048', '-nodes',
               '-out', '%s.csr' % certpath,
               '-keyout', keypath,
               '-subj', '/CN=Ipsilon Test %s' % name]
        subprocess.check_call(cmd,
                              stdout=self.stdout, stderr=self.stderr)
        cmd = ['openssl', 'ca', '-batch', '-notext', '-days', '2',
               '-md', 'sha256',
               '-subj', '/CN=Ipsilon Test %s' % name,
               '-outdir', os.path.join(self.testdir, 'certs'),
               '-keyfile', os.path.join(self.testdir, 'certs', 'root.key.pem'),
               '-cert', os.path.join(self.testdir, 'certs', 'root.cert.pem'),
               '-config', os.path.join(self.testdir, 'certs', 'openssl.conf'),
               '-in', '%s.csr' % certpath,
               '-out', certpath]
        ipaddr = addr
        if not ipaddr.startswith('127.'):
            # Lazy check whether this is a hostname (like in testnameid)
            # Note: this IP address might not be correct, but if when the
            # hostname is consistently used, that doesn't matter.
            # We just set it to a known value to make sure openssl doesn't
            # crash.
            ipaddr = '127.0.0.10'
        subprocess.check_call(cmd, env={'ADDR': addr, 'IPADDR': ipaddr},
                              stdout=self.stdout, stderr=self.stderr)

    def setup_idp_server(self, profile, name, addr, port, env):
        http_conf_file = self.setup_http(name, addr, port)
        logfile = os.path.join(self.testdir, name, 'logs', 'install.log')
        if env:
            env['LOGFILE'] = logfile
        else:
            env = {'LOGFILE': logfile}
        cmd = [self.pycmd,
               os.path.join(self.rootdir,
                            'ipsilon/install/ipsilon-server-install'),
               '--config-profile=%s' % profile]
        subprocess.check_call(cmd, env=env,
                              stdout=self.stdout, stderr=self.stderr)
        os.symlink(os.path.join(self.rootdir, 'ipsilon'),
                   os.path.join(self.testdir, 'lib', name, 'ipsilon'))
        # drop the Listen line written by ipsilon-server-install from
        # the config, as it will conflict with the address-specific
        # Listen line written by setup_http and break stuff
        isiconf = os.path.join(os.path.dirname(http_conf_file), "conf.d", "ipsilon-%s.conf" % name)
        with open(isiconf, 'r', encoding='utf-8') as isiconfh:
            lines = isiconfh.readlines()
        with open(isiconf, 'w', encoding='utf-8') as isiconfh:
            for line in lines:
                if line.startswith("Listen"):
                    continue
                isiconfh.write(line)

        return http_conf_file

    def setup_sp_server(self, profile, name, addr, port, env):
        http_conf_file = self.setup_http(name, addr, port)
        cmd = [self.pycmd,
               os.path.join(self.rootdir,
                            'ipsilon/install/ipsilon-client-install'),
               '--config-profile=%s' % profile]
        subprocess.check_call(cmd, env=env,
                              stdout=self.stdout, stderr=self.stderr)

        return http_conf_file

    def setup_pgdb(self, datadir, env):
        cmd = ['/usr/bin/pg_ctl', 'initdb', '-D', datadir, '-o', '-E UNICODE']
        subprocess.check_call(cmd, env=env,
                              stdout=self.stdout, stderr=self.stderr)
        auth = 'host all all 127.0.0.1/24 trust\n'
        filename = os.path.join(datadir, 'pg_hba.conf')
        with open(filename, 'a') as f:
            f.write(auth)

    def start_etcd_server(self, datadir, addr, clientport, srvport, env):
        env['ETCD_NAME'] = 'ipsilon'
        env['ETCD_DATA_DIR'] = datadir
        env['ETCD_LISTEN_CLIENT_URLS'] = 'http://%s:%s' % (addr, clientport)
        env['ETCD_LISTEN_PEER_URLS'] = 'http://%s:%s' % (addr, srvport)
        env['ETCD_FORCE_NEW_CLUSTER'] = 'true'
        env['ETCD_INITIAL_CLUSTER'] = 'ipsilon=http://%s:%s' % (addr, srvport)
        env['ETCD_ADVERTISE_CLIENT_URLS'] = 'http://%s:%s' % (addr, clientport)
        env['ETCD_INITIAL_ADVERTISE_PEER_URLS'] = 'http://%s:%s' % (addr,
                                                                    srvport)
        env['ETCD_ENABLE_V2'] = 'true'
        p = subprocess.Popen(['/usr/bin/etcd'],
                             env=env, preexec_fn=os.setsid,
                             stdout=self.stdout, stderr=self.stderr)
        self.processes.append(p)
        return p

    def start_http_server(self, conf, env):
        env['MALLOC_CHECK_'] = '3'
        env['MALLOC_PERTURB_'] = str(random.randint(0, 32767) % 255 + 1)
        env['REQUESTS_CA_BUNDLE'] = os.path.join(self.testdir, 'certs',
                                                 'root.cert.pem')
        p = subprocess.Popen(['/usr/sbin/httpd', '-DFOREGROUND', '-f', conf],
                             env=env, preexec_fn=os.setsid,
                             stdout=self.stdout, stderr=self.stderr)
        self.processes.append(p)
        return p

    def start_pgdb_server(self, datadir, rundir, log, addr, port, env):
        p = subprocess.Popen(['/usr/bin/pg_ctl', 'start', '-D', datadir, '-o',
                              '-k %s -c port=%s -c \
                               listen_addresses=%s' % (rundir, port, addr),
                              '-l', log, '-w'],
                             env=env, preexec_fn=os.setsid,
                             stdout=self.stdout, stderr=self.stderr)
        p.wait()
        with open(os.path.join(datadir, "postmaster.pid")) as pidfile:
            self.processes.append(int(pidfile.readline().strip()))
        for d in ['adminconfig', 'users', 'transactions', 'sessions',
                  'saml2.sessions.db']:
            cmd = ['/usr/bin/createdb', '-h', addr, '-p', port, d]
            subprocess.check_call(cmd, env=env,
                                  stdout=self.stdout, stderr=self.stderr)

    def setup_ldap(self, env):
        ldapdir = os.path.join(self.testdir, 'ldap')
        os.mkdir(ldapdir)
        with open(os.path.join(self.rootdir, 'tests/slapd.conf')) as f:
            t = Template(f.read())
            text = t.substitute({'ldapdir': ldapdir})
        filename = os.path.join(ldapdir, 'slapd.conf')
        with open(filename, 'w+') as f:
            f.write(text)
        subprocess.check_call(['/usr/sbin/slapadd', '-f', filename, '-l',
                               'tests/ldapdata.ldif'], env=env,
                              stdout=self.stdout, stderr=self.stderr)

        return filename

    def start_ldap_server(self, conf, addr, port, env):
        p = subprocess.Popen(['/usr/sbin/slapd', '-d', '0', '-f', conf,
                             '-h', 'ldap://%s:%s' % (addr, port)],
                             env=env, preexec_fn=os.setsid,
                             stdout=self.stdout, stderr=self.stderr)
        self.processes.append(p)

    def setup_kdc(self, env):

        # setup kerberos environment
        testlog = os.path.join(self.testdir, 'kerb.log')
        krb5conf = os.path.join(self.testdir, 'krb5.conf')
        kdcconf = os.path.join(self.testdir, 'kdc.conf')
        kdcdir = os.path.join(self.testdir, 'kdc')
        if os.path.exists(kdcdir):
            shutil.rmtree(kdcdir)
        os.makedirs(kdcdir)

        t = Template(KRB5_CONF_TEMPLATE)
        text = t.substitute({'TESTREALM': TESTREALM,
                             'TESTDOMAIN': TESTDOMAIN,
                             'TESTDIR': self.testdir,
                             'KDCDIR': kdcdir,
                             'KDC_DBNAME': KDC_DBNAME,
                             'WRAP_HOSTNAME': WRAP_HOSTNAME})
        with open(krb5conf, 'w+') as f:
            f.write(text)

        t = Template(KDC_CONF_TEMPLATE)
        text = t.substitute({'TESTREALM': TESTREALM,
                             'KDCDIR': kdcdir,
                             'KDCLOG': testlog,
                             'KDC_STASH': KDC_STASH})
        with open(kdcconf, 'w+') as f:
            f.write(text)

        kdcenv = {'PATH': '/sbin:/bin:/usr/sbin:/usr/bin',
                  'KRB5_CONFIG': krb5conf,
                  'KRB5_KDC_PROFILE': kdcconf}
        kdcenv.update(env)

        with (open(testlog, 'a')) as logfile:
            ksetup = subprocess.Popen(["kdb5_util", "create", "-s",
                                       "-r", TESTREALM, "-P", KDC_PASSWORD],
                                      stdout=logfile, stderr=logfile,
                                      env=kdcenv, preexec_fn=os.setsid)
        ksetup.wait()
        if ksetup.returncode != 0:
            raise ValueError('KDC Setup failed')

        kdcproc = subprocess.Popen(['krb5kdc', '-n'],
                                   env=kdcenv, preexec_fn=os.setsid,
                                   stdout=self.stdout, stderr=self.stderr)
        self.processes.append(kdcproc)

        return kdcenv

    def kadmin_local(self, cmd, env, logfile):
        ksetup = subprocess.Popen(["kadmin.local", "-q", cmd],
                                  stdout=logfile, stderr=logfile,
                                  env=env, preexec_fn=os.setsid)
        ksetup.wait()
        if ksetup.returncode != 0:
            raise ValueError('Kadmin local [%s] failed' % cmd)

    def setup_keys(self, env):

        testlog = os.path.join(self.testdir, 'kerb.log')

        svc_name = "HTTP/%s" % WRAP_HOSTNAME
        svc_keytab = os.path.join(self.testdir, HTTP_KTNAME)
        cmd = "addprinc -randkey -e %s %s" % (KEY_TYPE, svc_name)
        with (open(testlog, 'a')) as logfile:
            self.kadmin_local(cmd, env, logfile)
        cmd = "ktadd -k %s -e %s %s" % (svc_keytab, KEY_TYPE, svc_name)
        with (open(testlog, 'a')) as logfile:
            self.kadmin_local(cmd, env, logfile)

        usr_keytab = os.path.join(self.testdir, USER_KTNAME)
        cmd = "addprinc -randkey -e %s %s" % (KEY_TYPE, self.testuser)
        with (open(testlog, 'a')) as logfile:
            self.kadmin_local(cmd, env, logfile)
        cmd = "ktadd -k %s -e %s %s" % (usr_keytab, KEY_TYPE, self.testuser)
        with (open(testlog, 'a')) as logfile:
            self.kadmin_local(cmd, env, logfile)

        keys_env = {"KRB5_KTNAME": svc_keytab}
        keys_env.update(env)

        return keys_env

    def kinit_keytab(self, kdcenv):
        testlog = os.path.join(self.testdir, 'kinit.log')
        usr_keytab = os.path.join(self.testdir, USER_KTNAME)
        kdcenv['KRB5CCNAME'] = 'FILE:' + os.path.join(
            self.testdir, 'ccaches/user')
        with (open(testlog, 'a')) as logfile:
            logfile.write("\n%s\n" % kdcenv)
            ksetup = subprocess.Popen(["kinit", "-kt", usr_keytab,
                                       self.testuser],
                                      stdout=logfile, stderr=logfile,
                                      env=kdcenv, preexec_fn=os.setsid)
            ksetup.wait()
            if ksetup.returncode != 0:
                raise ValueError('kinit %s failed' % self.testuser)

    def wait(self):
        for p in self.processes:
            if isinstance(p, subprocess.Popen):
                pid = p.pid
            else:
                pid = p
            os.kill(pid, signal.SIGTERM)

    def setup_servers(self, env=None):
        raise NotImplementedError()

    def setup_step(self, message):
        """Method to inform setup step starting."""
        self.current_setup_step = message

    def run(self, env):
        """Method to run the test process and receive progress reports.

        The test process is run in a subprocess because it needs to be run with
        the socket and nss wrappers, which are used a LD_PRELOAD, which means
        the environment must be set before the process starts.

        The process running run() (Test Control process) communicates with the
        Test Process by reading specially formatted strings from standard out.

        All lines read from the test's stdout will be passed into TC.get_result
        to determine whether a test result was provided.
        """
        exe = self.execname
        if exe.endswith('c'):
            exe = exe[:-1]
        return self.run_and_collect([self.pycmd, exe], env)

    def run_and_collect(self, cmd, env):
        p = subprocess.Popen(
            cmd, env=env, universal_newlines=True,
            stdout=subprocess.PIPE, stderr=self.stderr)
        results = []
        for line in p.stdout:
            line = line[:-1]  # Strip newline
            result = TC.get_result(line)
            if result:
                if self.print_cases:
                    TC.output(result)
                results.append(result)
            else:
                if self.stdout is None:
                    print(line)
        return p.wait(), results
