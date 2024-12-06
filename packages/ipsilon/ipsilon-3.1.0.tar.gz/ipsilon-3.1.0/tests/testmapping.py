#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2017 Ipsilon project Contributors, for license see COPYING

from helpers.common import IpsilonTestBase  # pylint: disable=relative-import
from helpers.control import TC  # pylint: disable=relative-import
from helpers.http import HttpSessions  # pylint: disable=relative-import
import os
import pwd
from string import Template

# Test Attribute Mapping and Allowed Attributes and their per-SP
# overrides.


idp_g = {'TEMPLATES': '${TESTDIR}/templates/install',
         'CONFDIR': '${TESTDIR}/etc',
         'DATADIR': '${TESTDIR}/lib',
         'CACHEDIR': '${TESTDIR}/cache',
         'HTTPDCONFD': '${TESTDIR}/${NAME}/conf.d',
         'STATICDIR': '${ROOTDIR}',
         'BINDIR': '${ROOTDIR}/ipsilon',
         'WSGI_SOCKET_PREFIX': '${TESTDIR}/${NAME}/logs/wsgi'}


idp_a = {'hostname': '${ADDRESS}:${PORT}',
         'admin_user': '${TEST_USER}',
         'system_user': '${TEST_USER}',
         'instance': '${NAME}',
         'testauth': 'yes',
         'pam': 'no',
         'gssapi': 'no',
         'ipa': 'no',
         'server_debugging': 'True'}


sp_g = {'HTTPDCONFD': '${TESTDIR}/${NAME}/conf.d',
        'SAML2_TEMPLATE': '${TESTDIR}/templates/install/saml2/sp.conf',
        'CONFFILE': '${TESTDIR}/${NAME}/conf.d/ipsilon-%s.conf',
        'HTTPDIR': '${TESTDIR}/${NAME}/%s'}


sp_a = {'hostname': '${ADDRESS}',
        'saml_idp_metadata': 'https://127.0.0.10:45080/idp1/saml2/metadata',
        'saml_auth': '/sp',
        'saml_nameid': '${NAMEID}',
        'httpd_user': '${TEST_USER}'}

sp_list = [
    {'name': 'sp1', 'addr': '127.0.0.11', 'port': '45081'},
]


def convert_to_dict(envlist):
    values = {}
    for pair in envlist.split('\n'):
        if pair.find('=') > 0:
            (key, value) = pair.split('=', 1)
            if key.startswith('MELLON_') and not key.endswith('_0'):
                values[key] = value
    return values


def check_info_plugin(s, idp_name, urlbase, expected):
    """
    Logout, login, fetch SP page to get the info variables and
    compare the MELLON_ ones to what we expect.  IDP and NAMEID are
    ignored.
    """

    # Log out
    page = s.fetch_page(idp_name, '%s/%s?%s' % (
        urlbase, 'saml2/logout',
        'ReturnTo=%s/open/logged_out.html' % urlbase))
    page.expected_value('text()', 'Logged out')

    # Fetch the page (with implicit login)
    page = s.fetch_page(idp_name, '%s/sp/' % spurl)

    # Confirm that the expected values are in the output and that there
    # are no unexpected MELLON_ vars, and drop the _0 version.
    data = convert_to_dict(page.text)

    for key in expected:
        item = data.pop('MELLON_' + key)
        if item != expected[key]:
            raise ValueError('Expected %s, got %s' % (expected[key], item))

    # Ignore these attributes if they weren't tested for
    data.pop('MELLON_IDP', None)
    data.pop('MELLON_NAME_ID', None)
    data.pop('MELLON_ASSERTION_ID', None)

    if len(data) > 0:
        raise ValueError('Unexpected values %s' % data)


def fixup_sp_httpd(httpdir):
    location = """

AddOutputFilter INCLUDES .html

Alias /sp ${HTTPDIR}/sp

<Directory ${HTTPDIR}/sp>
    <IfModule mod_authz_core.c>
        Require all granted
    </IfModule>
    <IfModule !mod_authz_core.c>
        Order Allow,Deny
        Allow from All
    </IfModule>
    Options +Includes
</Directory>

Alias /open ${HTTPDIR}/open

<Directory ${HTTPDIR}/open>
</Directory>

"""
    index = """
<!--#printenv  -->
"""
    logged_out = """Logged out"""

    t = Template(location)
    text = t.substitute({'HTTPDIR': httpdir})
    with open(httpdir + '/conf.d/ipsilon-saml.conf', 'a') as f:
        f.write(text)

    os.mkdir(httpdir + '/sp')
    with open(httpdir + '/sp/index.html', 'w') as f:
        f.write(index)
    os.mkdir(httpdir + '/open')
    with open(httpdir + '/open/logged_out.html', 'w') as f:
        f.write(logged_out)


class IpsilonTest(IpsilonTestBase):

    def __init__(self):
        super(IpsilonTest, self).__init__('testmapping', __file__)

    def setup_servers(self, env=None):
        self.setup_step("Installing IDP server")
        name = 'idp1'
        addr = '127.0.0.10'
        port = '45080'
        idp = self.generate_profile(idp_g, idp_a, name, addr, port)
        conf = self.setup_idp_server(idp, name, addr, port, env)

        self.setup_step("Starting IDP's httpd server")
        self.start_http_server(conf, env)

        for spdata in sp_list:
            addr = spdata['addr']
            port = spdata['port']
            name = spdata['name']

            self.setup_step("Installing SP server %s" % name)
            sp_prof = self.generate_profile(sp_g, sp_a, name, addr, str(port))
            conf = self.setup_sp_server(sp_prof, name, addr, str(port), env)
            fixup_sp_httpd(os.path.dirname(conf))

            self.setup_step("Starting SP's httpd server")
            self.start_http_server(conf, env)


if __name__ == '__main__':

    idpname = 'idp1'
    user = pwd.getpwuid(os.getuid())[0]
    sp = sp_list[0]
    spurl = 'https://%s:%s' % (sp['addr'], sp['port'])

    # Set global mapping and allowed attributes, then test fetch from
    # SP.
    sess = HttpSessions()
    sess.add_server(idpname, 'https://127.0.0.10:45080', user, 'ipsilon')
    sess.add_server(sp['name'], spurl)

    with TC.case('Authenticate to IdP'):
        sess.auth_to_idp(idpname)

    with TC.case('Add SP Metadata to IdP'):
        sess.add_sp_metadata(idpname, sp['name'])

    with TC.case('Test default mapping and attrs'):
        expect = {
            'NAME_ID': user,
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
            'groups': user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set default global mapping'):
        sess.set_attributes_and_mapping(
            idpname,
            [['*', '*'],
             ['fullname', 'namefull']])

    with TC.case('Test global mapping'):
        expect = {
            'fullname': 'Test User %s' % user,
            'namefull': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
            'groups': user
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set default allowed attributes'):
        sess.set_attributes_and_mapping(
            idpname,
            [],
            ['namefull', 'givenname', 'surname'])

    with TC.case('Test global allowed attributes'):
        expect = {
            'namefull': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set SP allowed attributes'):
        sess.set_attributes_and_mapping(
            idpname, [['*', '*']],
            ['wholename', 'givenname', 'surname',
             'email', 'fullname'], sp['name'])

    with TC.case('Test SP allowed attributes'):
        expect = {
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set SP attribute mapping'):
        sess.set_attributes_and_mapping(
            idpname,
            [['*', '*'],
             ['fullname', 'wholename']],
            ['wholename', 'givenname',
             'surname',
             'email', 'fullname'],
            sp['name'])

    with TC.case('Test SP attribute mapping'):
        expect = {
            'wholename': 'Test User %s' % user,
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set SP URL attribute mapping'):
        sess.set_attributes_and_mapping(
            idpname,
            [['*', '*'],
             ['fullname', 'http://localhost/SAML/Name'],
             ['fullname', 'https://localhost/SAML/Name']],
            ['http://localhost/SAML/Name',
             'https://localhost/SAML/Name',
             'givenname',
             'surname',
             'email',
             'fullname'],
            sp['name'])

    with TC.case('Test SP URL attribute mapping'):
        expect = {
            'http://localhost/SAML/Name': 'Test User %s' % user,
            'https://localhost/SAML/Name': 'Test User %s' % user,
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set SP explicit mapping'):
        sess.set_attributes_and_mapping(
            idpname,
            [['fullname', 'wholename'],
             ['email', 'email']],
            ['wholename', 'email'],
            sp['name'])

    with TC.case('Test SP explicit mapping'):
        expect = {
            'wholename': 'Test User %s' % user,
            'email': '%s@example.com' % user,
            'NAME_ID': user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Set SP username mapping'):
        sess.set_attributes_and_mapping(
            idpname,
            [['*', '*'],
             ['fullname', 'wholename'],
             ['email', '_username']],
            ['wholename', 'givenname',
             'surname',
             'email', 'fullname'],
            sp['name'])

    with TC.case('Test SP username mapping'):
        expect = {
            'wholename': 'Test User %s' % user,
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
            'NAME_ID': '%s@example.com' % user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Drop SP attribute mapping'):
        sess.set_attributes_and_mapping(
            idpname, [],
            ['givenname', 'surname', 'email',
             'fullname'], sp['name'])

    with TC.case('Test SP attribute mapping with default allowed'):
        expect = {
            'fullname': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
            'email': '%s@example.com' % user,
        }
        check_info_plugin(sess, idpname, spurl, expect)

    with TC.case('Drop SP allowed attributes'):
        sess.set_attributes_and_mapping(idpname, [], [], sp['name'])

    with TC.case('Test mapping, should be back to global'):
        expect = {
            'namefull': 'Test User %s' % user,
            'surname': user,
            'givenname': u'Test User 一',
        }
        check_info_plugin(sess, idpname, spurl, expect)
