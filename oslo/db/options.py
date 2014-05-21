#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import copy

from oslo.config import cfg


database_opts = [
    cfg.StrOpt('sqlite_db',
               deprecated_group='DEFAULT',
               default='oslo.sqlite',
               help='The file name to use with SQLite.'),
    cfg.BoolOpt('sqlite_synchronous',
                deprecated_group='DEFAULT',
                default=True,
                help='If True, SQLite uses synchronous mode.'),
    cfg.StrOpt('backend',
               default='sqlalchemy',
               deprecated_name='db_backend',
               deprecated_group='DEFAULT',
               help='The back end to use for the database.'),
    cfg.StrOpt('connection',
               help='The SQLAlchemy connection string to use to connect to '
                    'the database.',
               secret=True,
               deprecated_opts=[cfg.DeprecatedOpt('sql_connection',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sql_connection',
                                                  group='DATABASE'),
                                cfg.DeprecatedOpt('connection',
                                                  group='sql'), ]),
    cfg.StrOpt('mysql_sql_mode',
               default='TRADITIONAL',
               help='The SQL mode to be used for MySQL sessions. '
                    'This option, including the default, overrides any '
                    'server-set SQL mode. To use whatever SQL mode '
                    'is set by the server configuration, '
                    'set this to no value. Example: mysql_sql_mode='),
    cfg.IntOpt('idle_timeout',
               default=3600,
               deprecated_opts=[cfg.DeprecatedOpt('sql_idle_timeout',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sql_idle_timeout',
                                                  group='DATABASE'),
                                cfg.DeprecatedOpt('idle_timeout',
                                                  group='sql')],
               help='Timeout before idle SQL connections are reaped.'),
    cfg.IntOpt('min_pool_size',
               default=1,
               deprecated_opts=[cfg.DeprecatedOpt('sql_min_pool_size',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sql_min_pool_size',
                                                  group='DATABASE')],
               help='Minimum number of SQL connections to keep open in a '
                    'pool.'),
    cfg.IntOpt('max_pool_size',
               deprecated_opts=[cfg.DeprecatedOpt('sql_max_pool_size',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sql_max_pool_size',
                                                  group='DATABASE')],
               help='Maximum number of SQL connections to keep open in a '
                    'pool.'),
    cfg.IntOpt('max_retries',
               default=10,
               deprecated_opts=[cfg.DeprecatedOpt('sql_max_retries',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sql_max_retries',
                                                  group='DATABASE')],
               help='Maximum db connection retries during startup. '
                    'Set to -1 to specify an infinite retry count.'),
    cfg.IntOpt('retry_interval',
               default=10,
               deprecated_opts=[cfg.DeprecatedOpt('sql_retry_interval',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('reconnect_interval',
                                                  group='DATABASE')],
               help='Interval between retries of opening a SQL connection.'),
    cfg.IntOpt('max_overflow',
               deprecated_opts=[cfg.DeprecatedOpt('sql_max_overflow',
                                                  group='DEFAULT'),
                                cfg.DeprecatedOpt('sqlalchemy_max_overflow',
                                                  group='DATABASE')],
               help='If set, use this value for max_overflow with '
                    'SQLAlchemy.'),
    cfg.IntOpt('connection_debug',
               default=0,
               deprecated_opts=[cfg.DeprecatedOpt('sql_connection_debug',
                                                  group='DEFAULT')],
               help='Verbosity of SQL debugging information: 0=None, '
                    '100=Everything.'),
    cfg.BoolOpt('connection_trace',
                default=False,
                deprecated_opts=[cfg.DeprecatedOpt('sql_connection_trace',
                                                   group='DEFAULT')],
                help='Add Python stack traces to SQL as comment strings.'),
    cfg.IntOpt('pool_timeout',
               deprecated_opts=[cfg.DeprecatedOpt('sqlalchemy_pool_timeout',
                                                  group='DATABASE')],
               help='If set, use this value for pool_timeout with '
                    'SQLAlchemy.'),
    cfg.BoolOpt('use_db_reconnect',
                default=False,
                help='Enable the experimental use of database reconnect '
                     'on connection lost.'),
    cfg.IntOpt('db_retry_interval',
               default=1,
               help='Seconds between database connection retries.'),
    cfg.BoolOpt('db_inc_retry_interval',
                default=True,
                help='If True, increases the interval between database '
                     'connection retries up to db_max_retry_interval.'),
    cfg.IntOpt('db_max_retry_interval',
               default=10,
               help='If db_inc_retry_interval is set, the '
                    'maximum seconds between database connection retries.'),
    cfg.IntOpt('db_max_retries',
               default=20,
               help='Maximum database connection retries before error is '
                    'raised. Set to -1 to specify an infinite retry '
                    'count.'),
]


def set_defaults(conf, connection=None, sqlite_db=None,
                 max_pool_size=None, max_overflow=None,
                 pool_timeout=None):
    """Set defaults for configuration variables."""

    conf.register_opts(database_opts, group='database')

    if connection is not None:
        conf.set_default('connection', connection, group='database')
    if sqlite_db is not None:
        conf.set_default('sqlite_db', sqlite_db, group='database')
    if max_pool_size is not None:
        conf.set_default('max_pool_size', max_pool_size, group='database')
    if max_overflow is not None:
        conf.set_default('max_overflow', max_overflow, group='database')
    if pool_timeout is not None:
        conf.set_default('pool_timeout', pool_timeout, group='database')


def list_opts():
    """Returns a list of oslo.config options available in the library.

    The returned list includes all oslo.config options which may be registered
    at runtime by the library.

    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by this library.

    :returns: a list of (group_name, opts) tuples
    """
    return [('database', copy.deepcopy(database_opts))]
