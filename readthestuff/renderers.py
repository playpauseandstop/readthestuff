"""
======================
readthestuff.renderers
======================

Implement various renderers for view functions.

"""

import asyncio

from functools import wraps

from aiohttp import web


def html_renderer(func, **kwargs):
    r"""Wrap function output into HTML Response.

    :param func: View function to execute.
    :param \*\*kwargs:
        Additional keyword arguments to be passed to Response instance.
    """
    @asyncio.coroutine
    @wraps(func)
    def wrapper(request):
        """Actual view function runner.

        :param request: Request instance.
        :type request: aiohttp.web.Request
        """
        return web.Response(text=func(request),
                            content_type='text/html',
                            **kwargs)
    return wrapper
