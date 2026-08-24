LOGGER_PRO = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)-8s] %(name)-15s (%(correlation_id)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["correlation_id"],
        },
        "rotate": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filters": ["correlation_id"],
            "filename": "{log_name}.log",
            "when": "midnight",
            "interval": 1,
            # Keep 30 days of rotated logs; without a limit these files grow forever.
            "backupCount": 30,
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console", "rotate"],
    },
    "loggers": {
        "django": {"level": "WARNING", "handlers": ["console", "rotate"], "propagate": False},
        "API": {"level": "WARNING", "handlers": ["console", "rotate"], "propagate": False},
        "TASK": {"level": "INFO", "handlers": ["console", "rotate"], "propagate": False},
    },
}
