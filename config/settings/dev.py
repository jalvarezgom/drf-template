from config.settings.base import *

########################
# Application Configuration
########################
INSTALLED_APPS.append("schema_graph")
INSTALLED_APPS.append("drf_spectacular")
INSTALLED_APPS.append("drf_spectacular_jsonapi")
ALLOWED_HOSTS = ["*"]
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
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = []
CORS_ALLOWED_ORIGIN = ["*"]

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
