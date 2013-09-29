"""
==================
readthestuff.users
==================

Module to work with users.

"""

import datetime
import logging
import uuid

from psycopg2 import Error as DatabaseError, ProgrammingError

from .app import app, db
from .utils import PickleRecord


logger = logging.getLogger(__name__)


def create():
    """
    Create dummy user and return it.
    """
    conn = db.getconn()
    cursor = conn.cursor()

    cursor.execute('SET TIMEZONE=%s', (app.settings.TIME_ZONE, ))

    sql = ('INSERT INTO users (username, created_at) '
           'VALUES (%s, %s) RETURNING id')
    username = str(uuid.uuid4())

    try:
        cursor.execute(sql, (username, datetime.datetime.now()))
    except DatabaseError:
        conn.rollback()
        extra = {'last_query': cursor.query, 'sql': sql, 'username': username}
        logger.error('Cannot create user', exc_info=True, extra=extra)
        raise
    else:
        created = cursor.fetchone()
        conn.commit()
    finally:
        db.putconn(conn, close=True)

    return get(created.id)


def delete_from_session(request):
    """
    Delete user from request's session and save changes.
    """
    if 'user' not in request.environ['beaker.session']:
        return

    del request.environ['beaker.session']['user']
    request.environ['beaker.session'].save()


def get(user_id):
    """
    Get user information from database.
    """
    conn = db.getconn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id, ))

    try:
        return PickleRecord(cursor.fetchone())
    except ProgrammingError:
        return None
    finally:
        db.putconn(conn, close=True)


def get_from_session(request):
    """
    Get user from request's session.
    """
    return request.environ['beaker.session'].get('user')


def store_to_session(request, user):
    """
    Save user to request.
    """
    request.environ['beaker.session']['user'] = user
    request.environ['beaker.session'].save()


def update(user, **kwargs):
    """
    Update user object in database.
    """
    args, parts = [], []
    conn = db.getconn()
    cursor = conn.cursor()

    for key, value in kwargs.iteritems():
        args.append(value)
        parts.append('{0} = %s'.format(key))

    args.append(user.id)
    sql = 'UPDATE users SET {0} WHERE id = %s'.format(', '.join(parts))

    try:
        cursor.execute(sql, args)
    except DatabaseError:
        conn.rollback()
        extra = {'args': args, 'last_query': cursor.query, 'sql': sql}
        logger.error('Cannot update user in database',
                     exc_info=True, extra=extra)
        raise
    else:
        conn.commit()
    finally:
        db.putconn(conn, close=True)

    return get(user.id)
