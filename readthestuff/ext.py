"""
================
readthestuff.ext
================

Extensions for Read the Stuff project, like init DB pool and setup cache and
sessions for web requests.

"""

import urlparse

from psycopg2.pool import ThreadedConnectionPool


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
