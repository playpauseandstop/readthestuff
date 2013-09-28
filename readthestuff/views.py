"""
==================
readthestuff.views
==================

Collection of all available view functions.

"""

from wtforms.validators import ValidationError

from .forms import ImportSubscriptionsForm


def import_subscriptions(request):
    """
    Import subscriptions from OPML file.
    """
    form = ImportSubscriptionsForm(request.POST)

    if request.method == 'POST' and form.validate():
        func = form.parse_subscriptions
        field = form.subscriptions.name

        try:
            subscriptions = func(request.POST[field])
        except ValidationError as err:
            form.errors['parsing'] = err
        else:
            return {'subscriptions': subscriptions}

    return {'form': form}


def index():
    """
    Index page.

    Show all necessary information about project for unathorized users.
    """
    return {'subscriptions_form': ImportSubscriptionsForm()}
