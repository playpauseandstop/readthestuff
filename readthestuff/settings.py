"""
=====================
readthestuff.settings
=====================

Settings for Read the Stuff project.

"""

from pathlib import Path

from rororo.logger import default_logging_dict, update_sentry_logging
from rororo.settings import (
    from_env,
    inject_settings,
    setup_logging,
    setup_timezone,
    to_bool,
)


# Initialize Path object for current directory
rel = Path(__file__).parent

# Project settings
DEBUG = to_bool(from_env('DEBUG', True))

# Date & time settings
TIME_ZONE = 'Europe/Kiev'

# Logging settings
loggers = ('aiohttp', 'gunicorn', 'readthestuff', 'rororo')
LOGGING = default_logging_dict(*loggers)
SENTRY_DSN = None

# Template settings
JINJA_FILTERS = {'format': format}
TEMPLATE_DIRS = (
    str((rel / 'templates').absolute()),
)

# Import local settings if any
inject_settings('readthestuff.settings_local', locals(), True)

# Update Sentry settings
update_sentry_logging(LOGGING, SENTRY_DSN, *loggers)

# Setup logging & timezone for Read the Stuff
setup_logging(LOGGING)
setup_timezone(TIME_ZONE)
