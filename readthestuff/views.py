"""
==================
readthestuff.views
==================

Collection of all available view functions.

"""

import logging

from psycopg2 import Error as DatabaseError
from wtforms.validators import ValidationError

from . import subscriptions
from .forms import ImportSubscriptionsForm


USER = type('User', (object, ), {'id': 1})
logger = logging.getLogger(__name__)


def import_subscriptions(request):
    """
    Import subscriptions from OPML file.
    """
    form = ImportSubscriptionsForm(request.POST)

    if request.method == 'POST' and form.validate():
        wrapper = request.POST[form.subscriptions.name]
        logger_extra = {'subscriptions_filename': wrapper.filename,
                        'user_id': USER.id}

        try:
            parsed = subscriptions.parse(wrapper)
            stored = subscriptions.store(USER, parsed)
        except DatabaseError:
            logger.warning('Import subscriptions caused database error',
                           exc_info=True, extra=logger_extra)
            return {'stored': False}
        except ValidationError as err:
            logger.warning('Import subscriptions caused validation error',
                           exc_info=True, extra=logger_extra)
            form.errors['parsing'] = err
        else:
            return {'stored': stored}

    return {'form': form}


def index():
    """
    Index page.

    Show all necessary information about project for unathorized users.
    """
    return {'subscriptions_form': ImportSubscriptionsForm()}
