"""
==================
readthestuff.forms
==================

Forms for Read the Stuff project.

"""

import logging

from collections import defaultdict

from lxml import etree
from wtforms.fields import FileField as BaseFileField
from wtforms.form import Form
from wtforms.validators import Regexp, ValidationError


logger = logging.getLogger(__name__)


class FileField(BaseFileField):
    """
    File field which understands WebOb's FieldStorage objects.
    """
    def process_formdata(self, data):
        """
        Validate only file's name not file's content.
        """
        self.data = data[0].filename


class ImportSubscriptionsForm(Form):
    """
    Import Feeds form.
    """
    subscriptions = FileField(
        'OPML File', [Regexp(r'^(.*).(opml|xml)$')],
        description='Please provide OPML or XML file with your subscriptions.'
    )

    def parse_subscriptions(self, wrapper):
        """
        Parse subscriptions in file wrapper.
        """
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

        # Get all user subscriptions
        subscriptions = defaultdict(list)

        for outline in doc.xpath('//outline[@xmlUrl]'):
            parent = outline.getparent()
            tags = []

            while parent.tag == 'outline':
                tags.append(parent.attrib['text'])
                parent = parent.getparent()

            tag = u'/'.join(tags)
            subscriptions[tag].append(outline.attrib)

        return subscriptions
