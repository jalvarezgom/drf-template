LOGGER_DEV = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"]},
        "API": {"level": "DEBUG", "handlers": ["console"]},
        "TEST": {"level": "DEBUG", "handlers": ["console"]},
        "TASK": {"level": "DEBUG", "handlers": ["console"]},
    },
}
