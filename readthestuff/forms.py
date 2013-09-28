"""
==================
readthestuff.forms
==================

Forms for Read the Stuff project.

"""

from wtforms.fields import FileField as BaseFileField
from wtforms.form import Form
from wtforms.validators import Regexp


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
