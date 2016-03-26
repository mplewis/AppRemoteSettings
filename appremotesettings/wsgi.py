"""
WSGI config for appremotesettings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appremotesettings.settings")

application = get_wsgi_application()

# https://devcenter.heroku.com/articles/django-assets
application = DjangoWhiteNoise(application)
