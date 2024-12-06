# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING
# -*- coding: utf-8 -*-

from ipsilon.login.common import LoginFormBase, LoginManagerBase, \
    LoginManagerInstaller
from ipsilon.util.plugin import PluginObject
from ipsilon.util import config as pconfig
import cherrypy
import logging


class TestAuth(LoginFormBase):

    def POST(self, *args, **kwargs):
        username = kwargs.get("login_name")
        password = kwargs.get("login_password")
        password += kwargs.get("login_otp", "")
        error = None

        if username and password:
            groups = []
            if ":" in username:
                userspec = username.split(":")
                username = userspec[0]
                for cmd in userspec[1:]:
                    if cmd.startswith("groups="):
                        groups = cmd[7:].split(",")
                    else:
                        err = f"testauth: unhandled username command {cmd} from username {username}"
                        cherrypy.log.error(err)
            if password == 'ipsilon':
                cherrypy.log("User %s successfully authenticated." % username)
                if not groups:
                    groups = [username]
                    groups.extend(self.lm.groups or [])
                testdata = {
                    'givenname': 'Test User 一',
                    'surname': username,
                    'fullname': 'Test User %s' % username,
                    'email': '%s@example.com' % username,
                    '_groups': groups
                }
                return self.lm.auth_successful(self.trans,
                                               username, 'password', testdata)
            else:
                cherrypy.log("User %s failed authentication." % username)
                error = "Authentication failed"
        else:
            error = "Username or password is missing"
            cherrypy.log.error("Error: " + error, severity=logging.ERROR)

        context = self.create_tmpl_context(
            username=username,
            error=error,
            error_password=not password,
            error_username=not username
        )
        self.lm.set_auth_error()
        return self._template('login/form.html', **context)


class LoginManager(LoginManagerBase):

    def __init__(self, *args, **kwargs):
        super(LoginManager, self).__init__(*args, **kwargs)
        self.name = 'testauth'
        self.service_name = 'testauth'
        self.path = 'testauth'
        self.page = None
        self.description = """
Form based TEST login Manager, DO NOT EVER ACTIVATE IN PRODUCTION """
        self.new_config(
            self.name,
            pconfig.String(
                'username text',
                'Text used to ask for the username at login time.',
                'Username'),
            pconfig.String(
                'password text',
                'Text used to ask for the password at login time.',
                'Password'),
            pconfig.String(
                'help text',
                'Text used to guide the user at login time.',
                'DISABLE IN PRODUCTION, USE ONLY FOR TEST ' +
                'Use any username they are all valid, "admin" gives ' +
                'administrative powers. ' +
                'Use the fixed password "ipsilon" for any user'),
            pconfig.List(
                'groups',
                'Extra groups')
        )


    @property
    def help_text(self):
        return self.get_config_value('help text')

    @property
    def username_text(self):
        return self.get_config_value('username text')

    @property
    def password_text(self):
        return self.get_config_value('password text')

    @property
    def groups(self):
        return self.get_config_value('groups')

    def get_tree(self, site):
        self.page = TestAuth(site, self, 'login/testauth')
        return self.page


class Installer(LoginManagerInstaller):

    def __init__(self, *pargs):
        super(Installer, self).__init__()
        self.name = 'testauth'
        self.pargs = pargs

    def install_args(self, group):
        group.add_argument('--testauth', choices=['yes', 'no'], default='no',
                           help='Configure PAM authentication')
        group.add_argument('--testauth-groups', action='store',
                           help='Extra groups for all testauth users')

    def configure(self, opts, changes):
        if opts['testauth'] != 'yes':
            return

        logging.debug(self.pargs)
        # Add configuration data to database
        po = PluginObject(*self.pargs)
        po.name = 'testauth'
        po.wipe_data()
        po.wipe_config_values()

        config = dict()
        if opts['testauth_groups'] is not None:
            cherrypy.log('testauth_groups is %s (%s)' % (
                opts['testauth_groups'], type(opts['testauth_groups'])))
            config['groups'] = opts['testauth_groups']
        po.save_plugin_config(config)

        # Update global config to add login plugin
        po.is_enabled = True
        po.save_enabled_state()
