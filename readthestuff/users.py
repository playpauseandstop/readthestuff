"""
==================
readthestuff.users
==================

Module to work with users.

"""

import logging
import uuid

from collections import namedtuple

from psycopg2 import Error as DatabaseError

from .app import db


logger = logging.getLogger(__name__)


def create():
    """
    Create dummy user and return it.
    """
    conn = db.getconn()
    cursor = conn.cursor()

    sql = 'INSERT INTO users (username) VALUES (%s) RETURNING id'
    username = str(uuid.uuid4())

    try:
        cursor.execute(sql, (username, ))
    except DatabaseError:
        conn.rollback()
        extra = {'last_query': cursor.query, 'sql': sql, 'username': username}
        logger.error('Cannot create user', exc_info=True, extra=extra)
        raise
    else:
        created = cursor.fetchone()
        conn.commit()

    cursor.execute('SELECT * FROM users WHERE id = %s', (created.id, ))
    user = cursor.fetchone()

    db.putconn(conn, close=True)
    return user


def delete_from_session(request):
    """
    Delete user from request's session and save changes.
    """
    if 'user' not in request.environ['beaker.session']:
        return

    del request.environ['beaker.session']['user']
    request.environ['beaker.session'].save()


def get_from_session(request):
    """
    Get user from request's session.
    """
    user_dict = request.environ['beaker.session'].get('user')

    if not user_dict:
        return user_dict

    user_tuple = namedtuple('User', user_dict.iterkeys())
    return user_tuple(*user_dict.itervalues())


def store_to_session(request, user):
    """
    Save user to request.
    """
    request.environ['beaker.session']['user'] = user._asdict()
    request.environ['beaker.session'].save()
