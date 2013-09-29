"""
==================
readthestuff.views
==================

Collection of all available view functions.

"""

import logging

from psycopg2 import Error as DatabaseError
from wtforms.validators import ValidationError

from . import entries, subscriptions, users
from .app import app, queue_entries
from .forms import ImportSubscriptionsForm


logger = logging.getLogger(__name__)


def done_setup(request):
    """
    Finish setup process.
    """
    user = users.get_from_session(request)

    if not user:
        return app.redirect('index')

    user = users.update(user, setup_done=True)
    users.store_to_session(request, user)

    queue_entries.enqueue(entries.fetch, user)
    return app.redirect('entries')


def entries_list(request, tag_id=None, subscription_id=None, only_unread=True):
    """
    Show user entries by tag or subscription ID.
    """
    user = users.get_from_session(request)

    if not user:
        return app.redirect('index')

    lookup = {'only_unread': only_unread,
              'subscription_id': subscription_id,
              'tag_id': tag_id}

    return {'entries': entries.get(user, **lookup),
            'subscriptions': subscriptions.get(user, False),
            'user': user}


def import_subscriptions(request):
    """
    Import subscriptions from OPML file.
    """
    user = users.get_from_session(request)

    if not user:
        return app.redirect('index')

    form = ImportSubscriptionsForm(request.POST)

    if request.method == 'POST' and form.validate():
        wrapper = request.POST[form.subscriptions.name]
        logger_extra = {'subscriptions_filename': wrapper.filename,
                        'user_id': user.id}

        try:
            parsed = subscriptions.parse(wrapper)
            stored = subscriptions.store(user, parsed)
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


def index(request):
    """
    Index page.
    """
    user = users.get_from_session(request)

    if user and user.setup_done:
        return app.redirect('entries')

    return {'subscriptions': subscriptions.get(user) if user else None,
            'subscriptions_form': ImportSubscriptionsForm(),
            'user': user}


def login(request):
    """
    Login with Dummy Test Account.
    """
    if 'user' in request.environ['beaker.session']:
        return app.redirect('index')

    users.store_to_session(request, users.create())
    return app.redirect('index')


def logout(request):
    """
    Logout currently authorized user.
    """
    if 'user' not in request.environ['beaker.session']:
        return app.redirect('index')

    users.delete_from_session(request)
    return app.redirect('index')
