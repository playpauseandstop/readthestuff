"""
================
readthestuff.app
================

WSGI application for Read the Stuff project.

"""

from beaker.middleware import SessionMiddleware
from pyelasticsearch import ElasticSearch
from raven import Client as SentryClient
from raven.middleware import Sentry
from redis import StrictRedis

from rororo.app import create_app

from . import settings
from .ext import init_db_pool, register_redis_to_beaker


# Create suitable WSGI application
app = create_app(settings)

# Setup PostgreSQL connection pool
db = init_db_pool(app)

# Setup connections to ElasticSearch and Redis
elastic = ElasticSearch(app.settings.ELASTICSEARCH_URL)
redis = StrictRedis.from_url(app.settings.REDIS_URL)

# Setup session support
register_redis_to_beaker()
app.wsgi_app = SessionMiddleware(app.wsgi_app, {
    'session.key': app.settings.SESSION_KEY,
    'session.secret': app.settings.SECRET_KEY,
    'session.type': 'ext:redis',
    'session.url': app.settings.REDIS_URL,
})

# Wrap WSGI application into Sentry middleware
if app.settings.SENTRY_DSN.startswith('https://'):
    sentry = SentryClient(app.settings.SENTRY_DSN)
    app.wsgi_app = Sentry(app.wsgi_app, client=sentry)
