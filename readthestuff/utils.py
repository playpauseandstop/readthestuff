"""
==================
readthestuff.utils
==================

Extensions and utilities for Read the Stuff project, like init DB pool and
setup cache and sessions for web requests.

"""

import os
import urlparse

try:
    import cPickle as pickle
except ImportError:
    import pickle

from beaker.cache import clsmap
from beaker.container import NamespaceManager
from beaker.exceptions import MissingCacheParameter
from beaker.synchronization import file_synchronizer
from beaker.util import verify_directory
from psycopg2.pool import ThreadedConnectionPool
from redis import StrictRedis


class PickleRecord(object):
    """
    Make any record returned from PostgreSQL by named tuple cursor available
    for pickling.
    """
    def __init__(self, record):
        """
        Store all record fields to object's dict.
        """
        for field in record._fields:
            setattr(self, field, getattr(record, field))


class RedisBeakerManager(NamespaceManager):
    """
    Support of Redis backend for Beaker session and cache managers.
    """
    def __init__(self, namespace, url, data_dir=None, lock_dir=None, **kwargs):
        """
        Initialize Redis connection.
        """
        NamespaceManager.__init__(self, namespace)

        if not url:
            raise MissingCacheParameter('URL setting for Redis is required.')

        if lock_dir:
            self.lock_dir = lock_dir
        elif data_dir:
            self.lock_dir = os.path.join(data_dir, 'container_redis_lock')

        if self.lock_dir:
            verify_directory(self.lock_dir)

        self.redis = StrictRedis.from_url(url)

    def __contains__(self, key):
        """
        Check that key present in cache.
        """
        return self.redis.get(self._format_key(key)) is not None

    def __delitem__(self, key):
        """
        Delete key from cache.
        """
        self.redis.delete(self._format_key(key))

    def __getitem__(self, key):
        """
        Return key from cache.
        """
        return pickle.loads(self.redis.get(self._format_key(key)))

    def __setitem__(self, key, value):
        """
        Set key to cache without any expiration.
        """
        return self.set_value(key, value)

    def do_remove(self):
        """
        Flush all keys from current db.
        """
        self.redis.flushdb()

    def get_creation_lock(self, key):
        """
        Setup creation lock.
        """
        identifier = u'/'.join(('rediscontainer', 'funclock',
                                self.namespace, key))
        return file_synchronizer(identifier=identifier, lock_dir=self.lock_dir)

    def keys(self):
        """
        Redis has value to iterate over all added keys to cache.
        """
        return self.redis.keys('*')

    def set_value(self, key, value, expiretime=None):
        """
        Set key to cache with optional expiration time.
        """
        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        self.redis.set(self._format_key(key), value, ex=expiretime)

    def _format_key(self, key):
        """
        Prepend namespace value to key.
        """
        return u':'.join(('beaker', self.namespace, key))


def init_db_pool(app):
    """
    Initialize database pool.
    """
    # Initial vars
    message = 'Cannot initialize DB pool without {0} option'.format
    options = app.settings.DATABASE_POOL_OPTIONS.copy()

    # Read min/max connections from pool options
    assert 'min_connections' in options, message('min_connections')
    min_connections = options.pop('min_connections')

    assert 'max_connections' in options, message('max_connections')
    max_connections = options.pop('max_connections')

    # Parse database URL
    urlparse.uses_netloc.append('postgres')
    parts = urlparse.urlparse(app.settings.DATABASE_URL)

    # Provide default keyword arguments for connect
    kwargs = {
        'user': parts.username,
        'password': parts.password,
        'host': parts.hostname,
        'port': int(parts.port or 5432),
        'database': parts.path.lstrip('/'),
    }

    # And update them with remained pool options
    kwargs.update(options)

    # Make and return connection pool
    return ThreadedConnectionPool(min_connections, max_connections, **kwargs)


def register_redis_to_beaker():
    """
    Register Redis manager to Beaker cache backends.
    """
    clsmap._clsmap['ext:redis'] = RedisBeakerManager
