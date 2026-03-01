"""
ASGI config for drf_template project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from config.environment import Environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", Environment.get_environment_settings())

application = get_asgi_application()
