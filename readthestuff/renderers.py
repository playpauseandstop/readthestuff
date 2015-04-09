"""
======================
readthestuff.renderers
======================

Implement various renderers for view functions.

"""

import asyncio

from functools import partial, wraps

import ujson

from aiohttp import web


RENDERERS = {
    # Extension: (Converter Function, Content Type)
    'html': (None, 'text/html'),
    'json': (ujson.dumps, 'application/json'),
    'plain': (None, 'text/plain'),
}


def renderer(ext, func, **kwargs):
    r"""Render view function output and construct valid Response.

    :param ext: Render extension: "html", "json" or "plain".
    :param func: View function to execute.
    :param \*\*kwargs:
        Additional keyword arguments to be passed to Response instance.
    """
    @asyncio.coroutine
    @wraps(func)
    def wrapper(request):
        """Actual view function runner.

        :param request: Request instance to pass to view function.
        :type request: aiohttp.web.Request
        """
        converter, content_type = RENDERERS[ext]

        output = func(request)
        output = converter(output) if callable(converter) else output

        return web.Response(text=output,
                            content_type=content_type,
                            **kwargs)

    return wrapper


html_renderer = partial(renderer, 'html')
json_renderer = partial(renderer, 'json')
plain_renderer = partial(renderer, 'plain')
