"""
==================
readthestuff.views
==================

Collection of all available view functions.

"""

from wtforms.validators import ValidationError

from . import subscriptions
from .forms import ImportSubscriptionsForm


USER = type('User', (object, ), {'id': 1})


def import_subscriptions(request):
    """
    Import subscriptions from OPML file.
    """
    form = ImportSubscriptionsForm(request.POST)

    if request.method == 'POST' and form.validate():
        wrapper = request.POST[form.subscriptions.name]

        try:
            parsed = subscriptions.parse(wrapper)
            stored = subscriptions.store(USER, parsed)
        except ValidationError as err:
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
