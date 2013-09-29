"""
====================
readthestuff.entries
====================

Module to get user entries from datastore and fetch entries from user's
subscriptions.

"""

import logging

from psycopg2 import ProgrammingError
from rororo.utils import make_debug

from .app import app, db, queue_entries
from .utils import PickleRecord


logger = logging.getLogger(__name__)
debug = make_debug(app.settings.DEBUG, instance=logger, level='info')


def get(user, **lookup):
    """
    Get entries for user by lookup.
    """
    return []


def fetch(user):
    """
    Fetch entries from user's subscriptions.
    """
    conn = db.getconn()
    cursor = conn.cursor()

    sql = ('SELECT s.id AS id, s.href AS href, s.received_at AS received_at '
           'FROM subscriptions AS s '
           'LEFT OUTER JOIN user_subscriptions AS us '
           'ON s.id = us.subscription_id '
           'WHERE us.user_id = %s')
    cursor.execute(sql, (user.id, ))

    try:
        items = cursor.fetchall()
    except ProgrammingError:
        extra = {'last_query': cursor.query, 'sql': sql, 'user_id': user.id}
        logger.warning('No user subscriptions to fetch',
                       exc_info=True, extra=extra)
        return False

    for item in items:
        queue_entries.enqueue(from_subscription, user, PickleRecord(item))

    return True


def from_subscription(user, subscription):
    """
    Fetch all entries from subscription and store them to database.
    """
    debug('Fetch entries for user from subscription',
          ', user: {user_id}, subscription: {subscription}',
          extra={'subscription': subscription.href,
                 'user_id': user.id})
