"""
=====================
readthestuff.settings
=====================

Main settings for Read the Stuff project.

"""

from rororo import GET


# Debug settings
DEBUG = True

# Datastore settings
ELASTICSEARCH_URL = 'http://127.0.0.1:9200/'
REDIS_URL = 'redis://127.0.0.1:6379/0'

# PEP8 settings
USE_PEP8 = True
PEP8_CLASS = 'flake8.engine.get_style_guide'

# Routes settings
ROUTES = (
    GET('/', 'readthestuff.views.index', name='index', renderer='index.html'),
)
