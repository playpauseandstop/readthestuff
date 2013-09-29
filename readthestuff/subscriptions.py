"""
==========================
readthestuff.subscriptions
==========================

Parsing subscriptions from OPML files and storing subscriptions to datastore.

"""

import logging
import operator
import time

from collections import defaultdict

from lxml import etree
from psycopg2 import Error as DatabaseError, ProgrammingError
from wtforms.validators import ValidationError

from rororo.utils import make_debug

from .app import app, db


logger = logging.getLogger(__name__)
debug = make_debug(app.settings.DEBUG, level='info', instance=logger)


def get(user):
    """
    Return list of user subscriptions from database.
    """
    conn = db.getconn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM user_subscriptions WHERE user_id = %s',
                   (user.id, ))

    try:
        return cursor.fetchall()
    except ProgrammingError:
        return []
    finally:
        db.putconn(conn, close=True)


def parse(wrapper):
    """
    Parse subscriptions from file wrapper's content.
    """
    # Initial vars
    start_time = time.time()

    # Read user file
    try:
        doc = etree.parse(wrapper.file)
    except etree.XMLSyntaxError:
        raise ValidationError('Cannot read OPML file. Looks like it '
                              'has invalid content.')

    # Get all user subscriptions and group them by tag
    counter = 0
    subscriptions = defaultdict(list)

    for outline in doc.xpath('//outline[@xmlUrl]'):
        parent = outline.getparent()
        tags = []

        while parent.tag == 'outline':
            tags.append(parent.attrib['text'])
            parent = parent.getparent()

        tag = u'/'.join(tags)
        data = dict(outline.attrib)

        if data['htmlUrl'].startswith('http://www.google.com/reader/view/'):
            data['htmlUrl'] = ''

        subscriptions[tag].append(data)
        counter += 1

    # Debug spent time and return results
    debug('Subscriptions file sucessfully parsed',
          ', number or subscriptions: {number_of_subscriptions}, time: '
          '{time:.4f}s', extra={'number_of_subscriptions': counter},
          start_time=start_time)
    return subscriptions


def store(user, user_subscriptions):
    """
    Store user subscriptions to database.

    We need to create if they still not exist in database subscription, tag,
    user subscription and user tag subscription.
    """
    # Initial vars
    start_time = time.time()

    # Get database connection and cursor
    conn = db.getconn()
    cursor = conn.cursor()

    # Prepare all data which should be stored in database
    subscriptions_set, tags_set = set(), set()
    user_subsciptions_dict, user_tag_subscriptions_dict = {}, {}

    for tag, data in user_subscriptions.iteritems():
        tags_set.add(tag)
        user_tag_subscriptions_dict[tag] = []

        for item in data:
            subscriptions_set.add(item['xmlUrl'])
            user_subsciptions_dict[item['xmlUrl']] = (
                item['htmlUrl'],
                item['title'],
                item['text']
            )
            user_tag_subscriptions_dict[tag].append(item['xmlUrl'])

    # Read already exist subscriptions
    cursor.execute('SELECT id, href FROM subscriptions WHERE href IN %s',
                   (tuple(subscriptions_set), ))

    try:
        subscriptions_mapping = {item.href: item.id
                                 for item in cursor.fetchall()}
    except ProgrammingError:
        subscriptions_mapping = {}

    subscriptions_set ^= set(subscriptions_mapping.iterkeys())

    # Store necessary subscriptions
    if subscriptions_set:
        sql = 'INSERT INTO subscriptions (href) VALUES (%s) RETURNING id'
        timer = time.time()

        for item in subscriptions_set:
            try:
                cursor.execute(sql, (item, ))
            except DatabaseError:
                conn.rollback()
                logger.error('Cannot store subscription to database',
                             exc_info=True,
                             extra={'last_query': cursor.query,
                                    'sql': sql,
                                    'subscription': item})
                raise
            else:
                stored = cursor.fetchone()
                subscriptions_mapping[item] = stored.id

        conn.commit()
        debug('Subscriptions stored to database',
              ', number of subscriptions: {number_of_subscriptions}, time: '
              '{time:.4f}s',
              extra={'number_of_subscriptions': len(subscriptions_set)},
              start_time=timer)

    # Store necessary tags
    cursor.execute('SELECT id, name FROM tags WHERE name IN %s',
                   (tuple(tags_set), ))
    try:
        tags_mapping = {item.name: item.id for item in cursor.fetchall()}
    except ProgrammingError:
        tags_mapping = {}
    tags_set ^= set(tags_mapping.iterkeys())

    if tags_set:
        sql = 'INSERT INTO tags (name) VALUES (%s) RETURNING id'
        timer = time.time()

        for item in tags_set:
            try:
                cursor.execute(sql, (item, ))
            except DatabaseError:
                conn.rollback()
                extra = {'last_query': cursor.query, 'sql': sql, 'tag': tag}
                logger.error('Cannot store tag to database',
                             exc_info=True, extra=extra)
                raise
            else:
                stored = cursor.fetchone()
                tags_mapping[item] = stored.id

        conn.commit()
        debug('Tags stored to database',
              ', number of tags: {number_of_tags}, time: {time:.4f}s',
              extra={'number_of_tags': len(tags_set)},
              start_time=timer)

    # Store necessary user subscriptions relations
    cursor.execute('SELECT id, subscription_id FROM user_subscriptions '
                   'WHERE user_id = %s AND subscription_id IN %s',
                   (user.id, tuple(subscriptions_mapping.values())))
    mapping = {item.subscription_id: item.id
               for item in cursor.fetchall()}

    sql = ('INSERT INTO user_subscriptions '
           '(user_id, subscription_id, title, link, summary) '
           'VALUES (%s, %s, %s, %s, %s) RETURNING id')
    counter, timer = 0, time.time()

    for href, item in user_subsciptions_dict.iteritems():
        sid = subscriptions_mapping[href]

        if sid in mapping:
            continue

        try:
            cursor.execute(sql, (user.id, sid, item[0], item[1], item[2]))
        except DatabaseError:
            conn.rollback()

            rev_mapping = dict(zip(subscriptions_mapping.values(),
                                   subscriptions_mapping.keys()))
            extra = {'last_query': cursor.query,
                     'link': item[1],
                     'sql': sql,
                     'summary': item[2],
                     'subscription': rev_mapping[sid],
                     'subscription_id': sid,
                     'title': item[0],
                     'user_id': user.id}

            logger.error('Cannot store user subscription to database',
                         exc_info=True, extra=extra)
            raise
        else:
            stored = cursor.fetchone()
            mapping[sid] = stored.id

            counter += 1

    if counter:
        conn.commit()
        debug('User subscriptions stored to database',
              ', number of items: {number_of_items}, time: {time:.4f}s',
              extra={'number_of_items': counter}, start_time=timer)

    # And finally store user tag subscriptions relations
    sql = ('INSERT INTO user_tag_subscriptions '
           '(user_id, tag_id, user_subscription_id) '
           'VALUES (%s, %s, %s)')
    counter, timer = 0, time.time()

    for tag, items in user_tag_subscriptions_dict.iteritems():
        tid = tags_mapping[tag]

        cursor.execute('SELECT user_subscription_id '
                       'FROM user_tag_subscriptions '
                       'WHERE user_id = %s AND tag_id = %s AND '
                       'user_subscription_id IN %s',
                       (user.id, tid, tuple(mapping.values())))
        ignored = map(operator.attrgetter('user_subscription_id'),
                      cursor.fetchall())

        for item in items:
            sid = subscriptions_mapping[item]

            if mapping[sid] in ignored:
                continue

            try:
                cursor.execute(sql, (user.id, tid, mapping[sid]))
            except DatabaseError:
                conn.rollback()

                rev_mapping = dict(zip(subscriptions_mapping.values(),
                                       subscriptions_mapping.keys()))
                extra = {'last_query': cursor.query,
                         'sql': sql,
                         'subscription': rev_mapping[sid],
                         'subscription_id': sid,
                         'tag': tag,
                         'tag_id': tid,
                         'user_id': user.id,
                         'user_subscription_id': mapping[sid]}

                logger.error('Cannot store user tag subscription to database',
                             exc_info=True, extra=extra)
            else:
                counter += 1

    if counter:
        conn.commit()
        debug('User tag subscriptions stored to database',
              ', number of items: {number_of_items}, time: {time:.4f}s',
              extra={'number_of_items': counter}, start_time=timer)

    # Don't forget to close current connection
    db.putconn(conn, close=True)

    debug('All subscriptions data stored to database', ', time: {time:.4f}s',
          start_time=start_time)
    return True
