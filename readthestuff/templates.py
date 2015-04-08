"""
======================
readthestuff.templates
======================

Prepare Jinja environment for rendering templates.

"""

from jinja2 import Environment, FileSystemLoader


#: Templates extensions where turn on Jinja autoescape by default
JINJA_HTML_TEMPLATES = ('.htm', '.html', '.xhtml', '.xml')


def jinja_autoescape(filename):
    """Should we activate autoescaping for given filename or not?

    :param filename: Filename of template to render.
    """
    return False if not filename else filename.endswith(JINJA_HTML_TEMPLATES)


def jinja_env(settings=None, app=None, **kwargs):
    r"""Prepare Jinja enviroment for rendering templates.

    Jinja environment could be prepared from app settings dict or from keyword
    arguments. When settings dict supplied, keyword arguments would be ignored.

    :param settings: Settings dict for initializing Jinja env.
    :param \*\*kwargs: Keyword arguments for initializing Jinja env.
    """
    # Read Jinja data from settings or kwargs
    if settings:
        template_dirs = settings.get('TEMPLATE_DIRS')
        jinja_options = settings.get('JINJA_OPTIONS')
        jinja_filters = settings.get('JINJA_FILTERS')
        jinja_globals = settings.get('JINJA_GLOBALS')
    else:
        template_dirs = kwargs.get('tempalte_dirs')
        jinja_options = kwargs.get('jinja_options')
        jinja_filters = kwargs.get('jinja_filters')
        jinja_globals = kwargs.get('jinja_globals')

    # Prepare Jinja options
    jinja_options = jinja_options or {}
    jinja_options.setdefault('autoescape', jinja_autoescape)

    template_dirs = template_dirs or ('templates', )
    jinja_options.setdefault('loader', FileSystemLoader(template_dirs))

    # Make Jinja environment
    env = Environment(**jinja_options)

    # Populate filters and globals from settings
    for key, value in (jinja_filters or {}).items():
        env.filters[key] = value
    for key, value in (jinja_globals or {}).items():
        env.globals[key] = value

    # Put app and settings to env globals if supplied
    if app:
        env.globals['app'] = app
    if settings:
        env.globals['settings'] = settings

    # Return prepared Jinja environment
    return env


def render_template(request, template_name, **context):
    r"""Render template to string.

    :param request: Request instance.
    :type request: aiohttp.web.Request
    :param template_name: Name of template to render.
    :param \*\*context: Context to pass to template.
    """
    jinja_env = request.app.get('jinja_env')
    assert jinja_env, 'Jinja environment not found in app context.'
    return jinja_env.get_template(template_name).render(**context)
