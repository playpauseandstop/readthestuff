"""
================
readthestuff.app
================

Backend application for Read the Stuff project.

"""

import logging

from pathlib import Path

from aiohttp import web

from rororo.settings import immutable_settings

from . import api, settings, views
from .renderers import html_renderer, json_renderer
from .templates import jinja_env


logger = logging.getLogger(__name__)
rel = Path(__file__).parent


class Application(web.Application):

    """Custom application to support debug mode from settings."""

    def __init__(self, **kwargs):
        """Store and use debug mode in request handler factory."""
        self._debug = kwargs.pop('debug', False)
        super().__init__(**kwargs)

    def make_handler(self, **kwargs):
        """Pass stored debug mode to request handler factory."""
        kwargs['access_log'] = self.logger
        kwargs['debug'] = self._debug
        kwargs['logger'] = self.logger
        kwargs['loop'] = self.loop
        return self._handler_factory(self, self.router, **kwargs)


def create_app(**options):
    r"""Factory for create ``aiohttp.web`` application.

    :param \*\*options: Additional options to apply to application.
    """
    settings_dict = immutable_settings(settings, **options)
    app = Application(logger=logger, debug=settings_dict['DEBUG'])

    app['jinja_env'] = jinja_env(settings_dict, app=app)
    app['settings'] = settings_dict

    # API URLs
    app.router.add_route('GET', '/api/', json_renderer(api.browser))

    # Pages & React Router URLs
    index_html = html_renderer(views.index)
    for path in ('/', '/about', '/contact', '/privacy', '/terms'):
        app.router.add_route('GET', path, index_html)

    # Static URLs
    app.router.add_static('/static', str((rel / 'static').absolute()))

    return app


#: Default Read the Stuff backend application
app = create_app()
