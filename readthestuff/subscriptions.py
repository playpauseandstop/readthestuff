"""
==========================
readthestuff.subscriptions
==========================

Parsing subscriptions from OPML files and storing subscriptions to datastore.

"""

import logging
import time

from collections import defaultdict

from lxml import etree
from wtforms.validators import ValidationError

from rororo.utils import make_debug

from .app import app


logger = logging.getLogger(__name__)
debug = make_debug(app.settings.DEBUG, level='info', instance=logger)


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
        wrapper.file.seek(0)
        logger.error('Invalid content of subscriptions file',
                     exc_info=True,
                     extra={'content': wrapper.file.read(),
                            'filename': wrapper.filename})
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


def store(user, subscriptions):
    """
    Store user subscriptions to datastore.
    """
