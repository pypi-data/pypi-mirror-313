#!/usr/bin/python
#
# Copyright (C) 2014-2017 Ipsilon project Contributors, for license see COPYING

from six.moves.urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from helpers.common import IpsilonTestBase  # pylint: disable=relative-import
from helpers.control import TC  # pylint: disable=relative-import
from helpers.http import HttpSessions  # pylint: disable=relative-import
import os
import pwd
from string import Template

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
        'httpd_user': '${TEST_USER}'}

sp2_g = {'HTTPDCONFD': '${TESTDIR}/${NAME}/conf.d',
         'SAML2_TEMPLATE': '${TESTDIR}/templates/install/saml2/sp.conf',
         'CONFFILE': '${TESTDIR}/${NAME}/conf.d/ipsilon-%s.conf',
         'HTTPDIR': '${TESTDIR}/${NAME}/%s'}

sp2_a = {'hostname': '${ADDRESS}',
         'saml_idp_url': 'https://127.0.0.10:45080/idp1',
         'admin_user': '${TEST_USER}',
         'admin_password': '${TESTDIR}/pw.txt',
         'saml_sp_name': 'sp2-test.example.com',
         'saml_auth': '/sp',
         'httpd_user': '${TEST_USER}'}

keyless_metadata = """<?xml version='1.0' encoding='UTF-8'?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#" cacheDuration="P7D"
    entityID="http://keyless-sp">
  <md:SPSSODescriptor
        protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:AssertionConsumerService
        Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        Location="http://keyless-sp/postResponse" index="0"/>
    <md:NameIDFormat>
urn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
  </md:SPSSODescriptor>
</md:EntityDescriptor>
"""


def fixup_sp_httpd(httpdir):
    location = """

Alias /sp ${HTTPDIR}/sp

<Directory ${HTTPDIR}/sp>
    <IfModule mod_authz_core.c>
        Require all granted
    </IfModule>
    <IfModule !mod_authz_core.c>
        Order Allow,Deny
        Allow from All
    </IfModule>
</Directory>
"""
    index = """WORKS!"""

    t = Template(location)
    text = t.substitute({'HTTPDIR': httpdir})
    with open(httpdir + '/conf.d/ipsilon-saml.conf', 'a') as f:
        f.write(text)

    os.mkdir(httpdir + '/sp')
    with open(httpdir + '/sp/index.html', 'w') as f:
        f.write(index)


class IpsilonTest(IpsilonTestBase):

    def __init__(self):
        super(IpsilonTest, self).__init__('test1', __file__)

    def setup_servers(self, env=None):
        self.setup_step("Installing IDP server")
        name = 'idp1'
        addr = '127.0.0.10'
        port = '45080'
        idp = self.generate_profile(idp_g, idp_a, name, addr, port)
        conf = self.setup_idp_server(idp, name, addr, port, env)

        self.setup_step("Starting IDP's httpd server")
        self.start_http_server(conf, env)

        self.setup_step("Installing first SP server")
        name = 'sp1'
        addr = '127.0.0.11'
        port = '45081'
        sp = self.generate_profile(sp_g, sp_a, name, addr, port)
        conf = self.setup_sp_server(sp, name, addr, port, env)
        fixup_sp_httpd(os.path.dirname(conf))

        self.setup_step("Starting first SP's httpd server")
        self.start_http_server(conf, env)

        self.setup_step("Installing second SP server")
        name = 'sp2-test.example.com'
        addr = '127.0.0.11'
        port = '45082'
        sp = self.generate_profile(sp2_g, sp2_a, name, addr, port)
        with open(os.path.dirname(sp) + '/pw.txt', 'a') as f:
            f.write('ipsilon')
        conf = self.setup_sp_server(sp, name, addr, port, env)
        os.remove(os.path.dirname(sp) + '/pw.txt')
        fixup_sp_httpd(os.path.dirname(conf))

        self.setup_step("Starting second SP's httpd server")
        self.start_http_server(conf, env)


if __name__ == '__main__':

    idpname = 'idp1'
    sp1name = 'sp1'
    sp2name = 'sp2-test.example.com'
    user = pwd.getpwuid(os.getuid())[0]

    sess = HttpSessions()
    sess.add_server(idpname, 'https://127.0.0.10:45080', user, 'ipsilon')
    sess.add_server(sp1name, 'https://127.0.0.11:45081')
    sess.add_server(sp2name, 'https://127.0.0.11:45082')

    with TC.case('Authenticate to IDP'):
        sess.auth_to_idp(idpname)

    with TC.case('Add first SP metadata to IDP'):
        sess.add_sp_metadata(idpname, sp1name)

    with TC.case('Make sure we send no RelayState if none was requested'):
        page = sess.fetch_page(idpname, 'https://127.0.0.11:45081/sp/',
                               follow_redirect=1)
        # Cut off the RelayState
        target = urlparse(page.result.headers['Location'])
        qs = parse_qs(target.query)
        del qs["RelayState"]
        target = target._replace(query=urlencode(qs, doseq=True))
        target = urlunparse(target)
        # The signature is now wrong and the next line will fail, but I don't
        # know how to rebuild it.
        # page = sess.fetch_page(idpname, target, post_forms=False)
        # data = sess.get_form_data(page, 'saml-response', ['name', 'value'])
        # if data[0] != 'https://127.0.0.11:45081/saml2/postResponse':
        #     TC.fail('Incorrect form found')
        # if 'RelayState' in data[2]:
        #     TC.fail('RelayState found in response form')
        # if len(data[3]) > 1 and data[3][1] == 'None':
        #     TC.fail('RelayState of None sent')
        # Note that at this point, we have not actually submitted the response

    with TC.case('Access first AP protected area'):
        page = sess.fetch_page(idpname, 'https://127.0.0.11:45081/sp/')
        page.expected_value('text()', 'WORKS!')

    with TC.case('Access second SP protected area'):
        page = sess.fetch_page(idpname, 'https://127.0.0.11:45082/sp/')
        page.expected_value('text()', 'WORKS!')

    with TC.case('Update second SP'):
        # This is a test to see whether we can update SAML SPs where the name
        # is an FQDN (includes hyphens and dots). See bug #196
        sess.set_attributes_and_mapping(idpname, [],
                                        ['namefull', 'givenname', 'surname'],
                                        spname=sp2name)

    newsess = HttpSessions()
    newsess.add_server(idpname, 'https://127.0.0.10:45080', user, 'wrong')
    with TC.case('Try authentication failure', should_fail=True):
        newsess.auth_to_idp(idpname)

    with TC.case('Add keyless SP metadata to IDP'):
        sess.add_metadata(idpname, 'keyless', keyless_metadata)
        page = sess.fetch_page(idpname, 'https://127.0.0.10:45080/idp1/admin/'
                                        'providers/saml2/admin')
        page.expected_value('//div[@id="row_provider_http://keyless-sp"]/'
                            '@title',
                            'WARNING: SP does not have signing keys!')
