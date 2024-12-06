#!/usr/bin/python
#
# Copyright (C) 2014-2017 Ipsilon project Contributors, for license see COPYING

from helpers.common import IpsilonTestBase  # pylint: disable=relative-import
from helpers.control import TC  # pylint: disable=relative-import
from helpers.http import HttpSessions  # pylint: disable=relative-import
import os
import pwd
import sqlite3
from string import Template
import time

from ipsilon.providers.openidc.store import OpenIDCStore, OpenIDCStaticStore

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
         'cleanup_interval': 1,
         'session_timeout': 1,  # We can't use floats here apparently.
         'server_debugging': 'True'}


sp_g = {'HTTPDCONFD': '${TESTDIR}/${NAME}/conf.d',
        'SAML2_TEMPLATE': '${TESTDIR}/templates/install/saml2/sp.conf',
        'CONFFILE': '${TESTDIR}/${NAME}/conf.d/ipsilon-%s.conf',
        'HTTPDIR': '${TESTDIR}/${NAME}/%s'}


sp_a = {'hostname': '${ADDRESS}',
        'saml_idp_metadata': 'https://127.0.0.10:45080/idp1/saml2/metadata',
        'saml_auth': '/sp',
        'httpd_user': '${TEST_USER}'}


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
        super(IpsilonTest, self).__init__('testcleanup', __file__)

    def setup_servers(self, env=None):
        self.setup_step("Installing IDP server")
        name = 'idp1'
        addr = '127.0.0.10'
        port = '45080'
        idp = self.generate_profile(idp_g, idp_a, name, addr, port)
        conf = self.setup_idp_server(idp, name, addr, port, env)

        self.setup_step("Starting IDP's httpd server")
        self.start_http_server(conf, env)

        self.setup_step("Installing SP server")
        name = 'sp1'
        addr = '127.0.0.11'
        port = '45081'
        sp = self.generate_profile(sp_g, sp_a, name, addr, port)
        conf = self.setup_sp_server(sp, name, addr, port, env)
        fixup_sp_httpd(os.path.dirname(conf))

        self.setup_step("Starting first SP's httpd server")
        self.start_http_server(conf, env)


if __name__ == '__main__':

    idpname = 'idp1'
    sp1name = 'sp1'
    user = pwd.getpwuid(os.getuid())[0]

    sess = HttpSessions()
    sess.add_server(idpname, 'https://127.0.0.10:45080', user, 'ipsilon')
    sess.add_server(sp1name, 'https://127.0.0.11:45081')

    db_url_base = f"sqlite:///{os.environ['TESTDIR']}/lib/idp1"

    with TC.case('Verify logged out state'):
        page = sess.fetch_page(idpname, 'https://127.0.0.10:45080/idp1/')
        page.expected_value('//div[@id="content"]/p/a/text()', 'Log In')

    with TC.case('Authenticating to IdP'):
        sess.auth_to_idp(idpname)

    with TC.case('Add SP Metadata to IdP'):
        sess.add_sp_metadata(idpname, sp1name)

    with TC.case('Access first SP Protected Area'):
        page = sess.fetch_page(idpname, 'https://127.0.0.11:45081/sp/')
        page.expected_value('text()', 'WORKS!')

    with TC.case('Verify logged in state'):
        page = sess.fetch_page(idpname, 'https://127.0.0.10:45080/idp1/')
        page.expected_value('//div[@id="content"]/p/a/text()', None)

    with TC.case('Checking that SAML2 sessions were created'):
        sess_db = os.path.join(os.environ['TESTDIR'],
                               'lib/idp1/saml2.sessions.db.sqlite')
        conn = sqlite3.connect(sess_db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM saml2_sessions;')
        if len(cur.fetchall()) == 0:
            raise ValueError('SAML2 sessions not created')
        conn.close()

    # Sessions are valid for one minute, and we clean up once per minute.
    # However, checking after two minute is kinda cutting it close, so we add ten
    # seconds to make sure the system has had time to clean up.
    print("Waiting for sessions to expire")
    time.sleep(130)

    with TC.case('Verify logged out state'):
        page = sess.fetch_page(idpname, 'https://127.0.0.10:45080/idp1/')
        page.expected_value('//div[@id="content"]/p/a/text()', 'Log In')

    with TC.case('Checking that SAML2 sessions were destroyed'):
        sess_db = os.path.join(os.environ['TESTDIR'],
                               'lib/idp1/saml2.sessions.db.sqlite')
        conn = sqlite3.connect(sess_db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM saml2_sessions;')
        sessions = cur.fetchall()
        if len(sessions) != 0:
            raise ValueError('SAML2 sessions left behind: %s' % sessions)


    with TC.case('Checking that refreshable OpenIDC tokens are not expired'):
        static_store = OpenIDCStaticStore(database_url=f"{db_url_base}/openidc.static.sqlite")
        store = OpenIDCStore(
                database_url=f"{db_url_base}/openidc.sqlite",
                static_store=static_store,
                token_lifetime={"access": 3600, "refresh": None},
        )

        # Remove existing tokens and userinfo
        for token_id in store.get_unique_data("token"):
            store.del_unique_data("token", token_id)
        for ui_id in store.get_unique_data("userinfo"):
            store.del_unique_data("userinfo", ui_id)

        # Prepare userinfo
        userinfocode = store.storeUserInfo({"name": "dummy"})

        # Create tokens
        token_refreshable = store.issueToken(
            client_id="client-id", username="username", scope=["openid"],
            issue_refresh=True, userinfocode=userinfocode
        )

        token_non_refreshable = store.issueToken(
            client_id="client-id", username="username", scope=["openid"],
            issue_refresh=False, userinfocode=userinfocode
        )

        assert len(store.get_unique_data("token")) == 2

        conn = sqlite3.connect(f"{os.environ['TESTDIR']}/lib/idp1/openidc.sqlite")
        cur = conn.cursor()

        expired_ts = int(time.time()) - 1

        # Setting tokens to expire
        cur.execute(
            "UPDATE token SET value = ? WHERE name = 'expires_at'",
            (expired_ts,)
        )
        conn.commit()
        conn.close()

        cleanup_count = store._cleanupExpiredTokens()

        if cleanup_count != 1:
            raise Exception(
                f"Should only have cleaned up 1 token, cleaned {cleanup_count}"
            )

        tokens = store.get_unique_data("token")
        assert len(tokens) == 1, f"{len(tokens)} tokens: {tokens!r}"
        if list(tokens.keys())[0] != token_refreshable["token_id"]:
            raise Exception("The refreshable token has been cleaned up")

        # Make sure the userinfo data has not been cleaned up
        userinfo = store.get_unique_data("userinfo")
        if len(userinfo) != 1:
            raise Exception("The userinfo data has been cleaned up")


    with TC.case('Checking that access tokens expire in the right amount of time'):
        static_store = OpenIDCStaticStore(database_url=f"{db_url_base}/openidc.static.sqlite")
        store = OpenIDCStore(
                database_url=f"{db_url_base}/openidc.sqlite",
                static_store=static_store,
                token_lifetime={"access": 1, "refresh": 1},
        )
        token = store.issueToken(
            client_id="client-id", username="username", scope=["openid"],
            issue_refresh=False, userinfocode=userinfocode
        )

        time.sleep(3)
        cleanup_count = store._cleanupExpiredTokens()

        assert cleanup_count == 1, f"{cleanup_count} tokens were cleaned up"
        assert token["token_id"] not in store.get_unique_data("token").keys()

    with TC.case("Checking that refresh tokens expire in the right amount of time"):
        token = store.issueToken(
            client_id="client-id", username="username", scope=["openid"],
            issue_refresh=True, userinfocode=userinfocode
        )
        time.sleep(3)
        cleanup_count = store._cleanupExpiredTokens()

        assert cleanup_count == 1, f"{cleanup_count} tokens were cleaned up"
        assert token["token_id"] not in store.get_unique_data("token").keys()
