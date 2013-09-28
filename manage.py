#!/usr/bin/env python
"""
======
manage
======

Management script for Read the Stuff project.

"""

from rororo.manager import manage

from readthestuff.app import app


if __name__ == '__main__':
    manage(app)
