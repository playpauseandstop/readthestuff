"""
=====================
readthestuff.settings
=====================

Main settings for Read the Stuff project.

"""

import os
import sys
import tempfile

from psycopg2.extras import NamedTupleCursor
from rororo import GET, POST
from rororo.utils import import_settings, setup_logging, setup_timezone


# Debug settings
DEBUG = False

# Datastore settings
DATABASE_URL = (
    'postgresql://readthestuff:readthestuff@127.0.0.1:5432/readthestuff'
)
DATABASE_POOL_OPTIONS = {
    'cursor_factory': NamedTupleCursor,
    'min_connections': 0,
    'max_connections': 20,
}
ELASTICSEARCH_URL = 'http://127.0.0.1:9200/'
REDIS_URL = 'redis://127.0.0.1:6379/0'

# Date and time settings
DISABLE_SETUP_TIMEZONE = True
TIME_ZONE = 'UTC'

# Logging settings
DISABLE_SETUP_LOGGING = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(levelname)s:%(name)s] %(message)s',
        },
        'naked': {
            'format': u'%(message)s',
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
            'stream': sys.stdout,
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'ERROR',
            'stream': sys.stderr,
        }
    },
    'loggers': {
        'readthestuff': {
            'handlers': ['stderr', 'stdout'],
            'level': 'DEBUG',
        },
        'rq': {
            'handlers': ['stderr', 'stdout'],
            'level': 'INFO',
        }
    }
}
LOCAL_LOGGING = {}
SENTRY_DSN = 'Sentry DSN URL'

# PEP8 settings
USE_PEP8 = True
PEP8_CLASS = 'flake8.engine.get_style_guide'

# Routes settings
ROUTES = (
    GET('/', 'index', renderer='index.html'),

    GET('/entries', 'entries', renderer='entries.html'),
    GET('/entries/all',
        'entries',
        default={'only_unread': False},
        name='all_entries',
        renderer='entries.html'),
    GET('/entries/subscription/{subscription_id:int}',
        'entries',
        name='subscription_entries',
        renderer='entries.html'),
    GET('/entries/subscription/{subscription_id:int}/all',
        'entries',
        default={'only_unread': False},
        name='all_subscription_entries',
        renderer='entries.html'),
    GET('/entries/tag/{tag_id:int}',
        'entries',
        name='tag_entries',
        renderer='entries.html'),
    GET('/entries/tag/{tag_id:int}/all',
        'entries',
        default={'only_unread': False},
        name='all_tag_entries',
        renderer='entries.html'),

    POST('/import',
         'import_subscriptions',
         renderer='import_subscriptions.html'),

    GET('/login', 'login'),
    GET('/logout', 'logout'),
)
ROUTES_VIEW_PREFIX = 'readthestuff.views'

# Queues settings
QUEUE_ENTRIES = 'readthestuff_entries'
QUEUE_SUBSCRIPTIONS = 'readthestuff_subscriptions'
QUEUES = (QUEUE_ENTRIES, QUEUE_SUBSCRIPTIONS)

# Session settings
SECRET_KEY = 'please provide proper secret key in local settings'
SESSION_DATA_DIR = os.path.join(tempfile.gettempdir(), 'readthestuff_beaker')
SESSION_KEY = 'readthestuff_sid'
SESSION_LOCK_DIR = None

# Import local settings
import_settings('readthestuff.settings_local', locals(), True)

# Setup Sentry logging
if SENTRY_DSN.startswith('https://'):
    LOGGING['handlers'].update({
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
        }
    })
    LOGGING['loggers']['readthestuff']['handlers'].append('sentry')
    LOGGING['loggers']['rq']['handlers'].append('sentry')

# Setup logging and timezone for both of WSGI and RQ parts
setup_logging(LOGGING, LOCAL_LOGGING)
setup_timezone(TIME_ZONE)
