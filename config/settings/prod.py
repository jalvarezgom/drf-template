from config.environment import Environment
from config.environs.prod import EnvironSettingsProd

if Environment._ENVIRON_SETTING is not EnvironSettingsProd:
    Environment._ENVIRON_SETTING = EnvironSettingsProd
    Environment.get_environment_settings()

from config.settings.base import *  # noqa: E402

########################
# Application Configuration
########################
ALLOWED_HOSTS = Environment.SETTINGS.APP.get_allowed_hosts()
INSTALLED_APPS = INSTALLED_APPS + []
MIDDLEWARE = MIDDLEWARE + []

########################
# DRF
########################
REST_FRAMEWORK = REST_FRAMEWORK

########################
# Authentication
########################
# AUTHENTICATION_BACKENDS = (
#     "django.contrib.auth.backends.ModelBackend",  # Auth basada en username/password
# )


########################
# CORS
########################
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = Environment.SETTINGS.APP.get_cors_allowed_origins()

# SESSION_COOKIE_SAMESITE = None
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "accept-language",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "cache-control",
    "connection",
    "sec-fetch-mode",
    "referer",
    "host",
    "HTTP-SECRET-KEY",
)
