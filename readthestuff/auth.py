"""
=================
readthestuff.auth
=================

Authentication views: Redirect to external provider page and process its
response (run auth callback).

"""

from urllib.parse import urlencode

from aiohttp import web

from . import constants


def google_login(request):
    """Redirect to Google OAuth page."""
    settings = request.app['settings']
    query = urlencode((
        ('response_type', constants.GOOGLE_OAUTH_RESPONSE_TYPE),
        ('client_id', settings['GOOGLE_OAUTH_CLIENT_ID']),
        ('redirect_uri', settings['GOOGLE_OAUTH_REDIRECT_URI']),
        ('scope', constants.GOOGLE_OAUTH_SCOPE),
        ('state', constants.GOOGLE_OATUH_STATE),
        ('approval_prompt', constants.GOOGLE_OAUTH_APPROVAL_PROMPT),
    ))
    raise web.HTTPFound('?'.join((constants.GOOGLE_OAUTH_AUTH_URL, query)))


def google_login_callback(request):
    """Validate response from Google OAuth service and login user to site."""
