"""
================
readthestuff.app
================

Backend application for Read the Stuff project.

"""

import logging

from aiohttp import web

from rororo.settings import immutable_settings

from . import settings, views
from .renderers import html_renderer
from .templates import jinja_env


logger = logging.getLogger(__name__)


class Application(web.Application):

    """Custom application to support debug mode."""

    def __init__(self, **kwargs):
        """Store and use debug mode in request handler factory."""
        self._debug = kwargs.pop('debug', False)
        super().__init__(**kwargs)

    def make_handler(self, **kwargs):
        """Pass stored debug mode to request handler factory."""
        kwargs['debug'] = self._debug
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

    app.router.add_route('GET', '/', html_renderer(views.index))

    return app


#: Default Read the Stuff backend application
app = create_app()
