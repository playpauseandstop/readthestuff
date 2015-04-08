"""
==================
readthestuff.views
==================

Implement views which renders templates for Read the Stuff project.

"""

from .templates import render_template


def index(request):
    """Render index template."""
    return render_template(request, 'index.html')
