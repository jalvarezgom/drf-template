from config.settings.base import *

########################
# Application Configuration
########################
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
TOKEN_EXPIRED_AFTER_SECONDS = 60 * 60 * 12  # 12h


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
