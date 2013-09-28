"""
=====================
readthestuff.settings
=====================

Main settings for Read the Stuff project.

"""

import sys

from rororo import GET, POST
from rororo.utils import import_settings


# Debug settings
DEBUG = False

# Datastore settings
ELASTICSEARCH_URL = 'http://127.0.0.1:9200/'
REDIS_URL = 'redis://127.0.0.1:6379/0'

# Date and time settings
TIME_ZONE = 'UTC'

# Logging settings
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
    }
}
LOCAL_LOGGING = {}
SENTRY_DSN = 'Sentry DSN URL'

# PEP8 settings
USE_PEP8 = True
PEP8_CLASS = 'flake8.engine.get_style_guide'

# Routes settings
ROUTES = (
    GET('/', 'readthestuff.views.index', name='index', renderer='index.html'),
    POST('/import',
         'readthestuff.views.import_subscriptions',
         name='import_subscriptions',
         renderer='import_subscriptions.html'),
)

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
