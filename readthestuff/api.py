"""
================
readthestuff.api
================

API views for Read the Stuff project.

"""


def browser(request):
    """Browse over available API URLs due to user logged in status."""
    return {'urls': {}, 'user': {}}
