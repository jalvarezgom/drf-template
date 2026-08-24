LOGGER_DEV = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)-8s] %(name)-15s (%(correlation_id)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["correlation_id"],
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "API": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "TEST": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "TASK": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
}
