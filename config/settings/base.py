from config.environment import Environment

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Environment.BASE_DIR
BASE_URL = Environment.BASE_URL

########################
# Application Configuration
########################
SECRET_KEY = Environment.SECRET_KEY
DEBUG = Environment.SETTINGS.DEBUG
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # "psqlextra",
    "config",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "sequences.apps.SequencesConfig",
    # "drf_spectacular",
    # "drf_spectacular_jsonapi",
    "django_guid",
    "rest_framework_json_api",
    "django.contrib.sites",
    # "rest_framework.authtoken", # if used native DRF token auth
    "django_celery_beat", # Celery periodic tasks
    "django_celery_results", # Celery task results
    "actstream",  # Audit package
    "apps.authentication",
    "apps.task",
    "apps.app_1",
    "apps.app_2",
    "apps.app_3",
]
SITE_ID = 1
MIDDLEWARE = [
    "django_guid.middleware.guid_middleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "api.middleware.APILoggingMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "config" / "email_templates" / "html"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"

# Database
if "sqlite3" in Environment.SETTINGS.DB.ENGINE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": Environment.SETTINGS.DB.ENGINE,
            "NAME": Environment.SETTINGS.DB.NAME,
            "USER": Environment.SETTINGS.DB.USER,
            "PASSWORD": Environment.SETTINGS.DB.PASSWORD,
            "HOST": Environment.SETTINGS.DB.HOST,
            "PORT": Environment.SETTINGS.DB.PORT,
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {
        "NAME": "apps.core.validators.length.MaximumLengthValidator",
        "OPTIONS": {
            "max_length": 72,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "apps.core.validators.characters.SpecialCharactersValidator",
        "OPTIONS": {
            "min_special_characters": 1,
        },
    },
    {
        "NAME": "apps.core.validators.characters.UppercaseValidator",
        "OPTIONS": {
            "min_uppercase": 1,
        },
    },
    {
        "NAME": "apps.core.validators.characters.LowercaseValidator",
        "OPTIONS": {
            "min_lowercase": 1,
        },
    },
    {
        "NAME": "apps.core.validators.numerics.NumericValidator",
        "OPTIONS": {
            "min_numeric": 1,
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = []

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular_jsonapi.schemas.openapi.JsonApiAutoSchema",
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.authentication.auth.secret_key.SecretKeyAuthentication",
        "apps.authentication.auth.expiring_token.ExpiringTokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.DjangoModelPermissions",
    ),
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'PAGE_SIZE': 10,
    "DEFAULT_PAGINATION_CLASS": 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        'rest_framework.parsers.JSONParser',
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework_json_api.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.backends.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json',
    "JSON_API_UNIFORM_EXCEPTIONS": True,
}

DJANGO_GUID = {
    "GUID_HEADER_NAME": "Transaction-ID",
    "VALIDATE_GUID": True,
    "RETURN_HEADER": True,
    "EXPOSE_HEADER": True,
    "INTEGRATIONS": [],
    "IGNORE_URLS": [],
    "UUID_LENGTH": 32,
}

########################
# API Doc Configuration
########################
SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "API Description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "PREPROCESSING_HOOKS": [
        "drf_spectacular_jsonapi.hooks.fix_nested_path_parameters",
    ],
    # "POSTPROCESSING_HOOKS": [
    #     "api.schema_hooks.attach_task_202_examples",
    # ],
}

########################
# Audit Configuration
# If you need to add an auditing or tracking system, you can use the library 'django-activity-stream'.
########################
# ACTSTREAM_SETTINGS = {
#     'MANAGER': 'authentication.managers.audit.AuditManager',
#     'FETCH_RELATIONS': True,
#     'USE_JSONFIELD': True,
# }


########################
# Authentication
########################
AUTH_USER_MODEL = "authentication.User"  # Variable para cambiar el modelo usado para la autenticacion
TOKEN_EXPIRED_AFTER_SECONDS = Environment.SETTINGS.TOKEN_EXPIRED_AFTER_SECONDS #60 * 60  # 1 hour
AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.RemoteUserBackend', # Auth basada en usuario de Windows
    "apps.authentication.backends.email_password.EmailPasswordBackend",  # Auth basada en email/password
    "django.contrib.auth.backends.ModelBackend",  # Auth basada en user/password
)

########################
# LOGGING
########################
LOGGING = Environment.LOGGER_CFG

########################
# CORS
########################
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#  'http://localhost:80',
# ]
# CORS_ALLOWED_ORIGIN = [
#  'http://localhost:80',
# ]

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
)
