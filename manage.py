#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appremotesettings.settings")

    # https://github.com/etianen/django-herokuapp/blob/master/README.rst#running-your-site-in-the-heroku-environment
    from herokuapp.env import load_env
    load_env(__file__, 'appremotesettings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
