#!/usr/bin/python
#
# Copyright (C) 2015 Ipsilon project Contributors, for license see COPYING

import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import ipsilon.util.sessions
from ipsilon.util.data import AdminStore, Store, UserStore, TranStore
from ipsilon.util.sessions import SqlSession, EtcdSession
from ipsilon.root import Root

import logging

logger = logging.getLogger(__name__)


def _upgrade_database(datastore):
    """
    This function actually triggers the update on the datastore class.
    Returns True for success, False for failure, and None if it didn't do
    anything because the datastore is readonly, as happens with configfiles.
    """
    logger.info('Considering datastore %s', datastore.__class__.__name__)
    if datastore.is_readonly:
        logger.warning('Datastore is readonly. Please fix manually!')
        return None
    # pylint: disable=protected-access
    current_version = datastore._get_schema_version()
    # pylint: disable=protected-access
    code_schema_version = datastore._code_schema_version()
    upgrade_required = False
    if current_version is None:
        # Initialize schema
        logger.info('Initializing schema for %s',
                    datastore.__class__.__name__)
        upgrade_required = True
    elif current_version != code_schema_version:
        logger.info('Upgrading schema for %s', datastore.__class__.__name__)
        upgrade_required = True
    else:
        logger.info('Schema for %s is up-to-date',
                    datastore.__class__.__name__)
    if upgrade_required:
        try:
            datastore.upgrade_database()
        except Exception as ex:  # pylint: disable=broad-except
            # Error upgrading database
            logger.error('Error upgrading datastore: %s', ex)
            return False
        else:
            # Upgrade went OK
            return True
    else:
        return True


def upgrade_failed():
    logger.error('Upgrade failed. Please fix errors above and retry')
    raise RuntimeError('Upgrading failed')


def execute_upgrade(cfgfile):
    cherrypy.lib.sessions.SqlSession = ipsilon.util.sessions.SqlSession
    cherrypy.lib.sessions.EtcdSession = ipsilon.util.sessions.EtcdSession
    cherrypy.config.update(cfgfile)

    # pylint: disable=protected-access
    Store._is_upgrade = True

    adminstore = AdminStore()
    # First try to upgrade the config store before continuing
    if _upgrade_database(adminstore) not in [True, None]:
        return upgrade_failed()

    admin_config = adminstore.load_config()
    for option in admin_config:
        cherrypy.config[option] = admin_config[option]

    # Initialize a minimal env
    template_env = Environment(
        loader=FileSystemLoader(
            os.path.join(cherrypy.config['base.dir'],
                         'templates')),
        autoescape=True)
    root = Root('default', template_env)

    # Handle the session store if that is Sql
    logger.info('Handling sessions datastore')
    sesstype = cherrypy.config['tools.sessions.storage_type'].lower()
    if sesstype == 'sql':
        dburi = cherrypy.config['tools.sessions.storage_dburi']
        SqlSession.setup(storage_dburi=dburi)
        if _upgrade_database(SqlSession._store) not in [True, None]:
            return upgrade_failed()
    elif sesstype == 'etcd':
        dburi = cherrypy.config['tools.sessions.storage_dburi']
        EtcdSession.setup(storage_dburi=dburi)
        if _upgrade_database(EtcdSession._store) not in [True, None]:
            return upgrade_failed()
    else:
        logger.info('File based, skipping')

    # Now handle the rest of the default datastores
    for store in [UserStore, TranStore]:
        store = store()
        logger.info('Handling default datastore %s',
                    store.__class__.__name__)
        if _upgrade_database(store) not in [True, None]:
            return upgrade_failed()

    # And now datastores for any of the plugins
    userstore = UserStore()
    for facility in ['provider_config',
                     'login_config',
                     'info_config',
                     'authz_config']:
        for plugin in root._site[facility].enabled:
            logger.info('Handling plugin %s', plugin)
            if plugin not in root._site[facility].available:
                logger.error('Plugin was unavailable')
                continue
            plugin = root._site[facility].available[plugin]
            logger.info('Creating plugin AdminStore table')
            adminstore.create_plugin_data_table(plugin.name)
            logger.info('Creating plugin UserStore table')
            userstore.create_plugin_data_table(plugin.name)
            for store in plugin.used_datastores():
                logger.info('Handling plugin datastore %s',
                            store.__class__.__name__)
                if _upgrade_database(store) not in [True, None]:
                    return upgrade_failed()

    # We are done with the init/upgrade
    # pylint: disable=protected-access
    Store._is_upgrade = False
