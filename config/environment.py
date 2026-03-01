import logging
import os
from datetime import datetime
from logging import Logger, config
from pathlib import Path

from apps.core.managers.google_email import GoogleEmailManager
from apps.core.managers.s3 import S3StorageService
from config.environs.base import EnvironSettings
from config.environs.dev import EnvironSettingsDev
from config.environs.test import EnvironSettingsTest
from config.loggers.dev import LOGGER_DEV
from config.loggers.pro import LOGGER_PRO


class EnvironmentMode:
    API = "API"
    TASK = "TASK"
    DJANGO = "django"
    TEST = "TEST"


class Environment:
    # Settings
    SETTINGS: EnvironSettings = None
    _ENVIRON_SETTING = EnvironSettingsDev
    LOAD_STATUS = False

    # Environment
    ENV = None
    ENV_MODE = EnvironmentMode.API
    __ENV_DEV = "DEV"
    __ENV_PRO = "PROD"

    # API
    BASE_URL = "api/"
    BASE_DIR = Path(__file__).parent.resolve()
    SECRET_KEY = None

    # Logger
    LOGGER_CFG = None
    logger: Logger = None

    @classmethod
    def is_dev_mode(cls):
        return cls.ENV == cls.__ENV_DEV

    @classmethod
    def is_prod_mode(cls):
        return cls.ENV == cls.__ENV_PRO

    @classmethod
    def get_environment_settings(cls, django_argv=None):
        cls.prepare(django_argv)
        setting = f"config.settings.{cls.SETTINGS.ENV}".lower()
        return setting

    @classmethod
    def prepare(cls, django_argv, *, ignore_email=None):
        if not cls.LOAD_STATUS:
            cls.__prepare_environ(django_argv)
            cls.__prepare_logger()
            cls.__check_execute_conditions(ignore_email)
            cls.__prepare_email_connection()
            cls.__prepare_s3_storage()
            cls.logger.info(f"[Environment] {cls.SETTINGS.APP_NAME} is UP")
            cls.logger.info(f"[Environment] Environment: {cls.ENV} | Mode: {cls.ENV_MODE}")
            cls.logger.info(f"[Environment] Setting: {f'config.settings.{cls.SETTINGS.__class__.__name__}'.lower()}")
            cls.logger.info(f"[Environment] Sentry status: {cls.SETTINGS.SENTRY.USE}")
            cls.LOAD_STATUS = True

    @classmethod
    def __prepare_environ(cls, django_argv):
        command = "runserver" if (django_argv is None or len(django_argv) == 1) else django_argv[1]
        if command == "runserver":  # TODO: Adaptar para gunicurn
            cls.ENV_MODE = EnvironmentMode.API
        elif cls._ENVIRON_SETTING == EnvironSettingsTest:
            cls.ENV_MODE = EnvironmentMode.TEST
        elif command in []:
            cls.ENV_MODE = EnvironmentMode.TASK
        else:
            cls.ENV_MODE = EnvironmentMode.DJANGO
        cls.SETTINGS = cls._ENVIRON_SETTING()
        cls.DIRECTORIES = cls.SETTINGS.DIRECTORY
        cls.SECRET_KEY = cls.SETTINGS.SECRET_KEY
        cls.ENV = cls.SETTINGS.ENV

    @classmethod
    def __prepare_logger(cls):
        if cls._ENVIRON_SETTING == EnvironSettingsTest:
            cls.LOGGER_CFG = LOGGER_DEV
        elif cls.is_dev_mode():
            cls.LOGGER_CFG = LOGGER_DEV
        else:
            cls.LOGGER_CFG = LOGGER_PRO
        cls.__apply_custom_action_to_logger()
        config.dictConfig(cls.LOGGER_CFG)
        cls.logger = logging.getLogger(cls.ENV_MODE)
        cls.logger.debug("[Environment] Logger configurado")

    @classmethod
    def __apply_custom_action_to_logger(cls):
        handlers = cls.LOGGER_CFG.get("handlers")
        if handlers is None:
            raise ValueError("[Environment] Logger configuration must include 'handlers' section")
        rotate_handler = handlers.get("rotate")
        if rotate_handler:
            log_name = cls.__get_log_filename()
            if cls.DIRECTORIES.LOGS:
                if not os.path.exists(cls.DIRECTORIES.LOGS):
                    os.makedirs(cls.DIRECTORIES.LOGS)
                rotate_handler["filename"] = f"{cls.DIRECTORIES.LOGS}/{log_name}.log"
            else:
                rotate_handler["filename"] = rotate_handler["filename"].format(log_name=cls.__get_log_filename())

    @classmethod
    def __get_log_filename(cls):
        date = datetime.now()
        log_filename = f"{cls.SETTINGS.APP_NAME}_{cls.ENV_MODE}_{date:%Y%m%d}"
        return log_filename

    @classmethod
    def __check_execute_conditions(cls, ignore_email):
        cls._ignore_email = False if cls.ENV_MODE == EnvironmentMode.API else ignore_email
        cls.logger.info(f"[Environment] Ignore Email: {ignore_email}")

    @classmethod
    def __prepare_email_connection(cls):
        if not cls._ignore_email and cls.SETTINGS.EMAIL.USE:
            cls.EMAIL_MANAGER = GoogleEmailManager(_username=Environment.SETTINGS.EMAIL.USER, _send_emails=Environment.SETTINGS.EMAIL.SEND_EMAILS)
            cls.EMAIL_MANAGER.init_connection(
                project_id=cls.SETTINGS.EMAIL.PROJECT_ID, client_id=cls.SETTINGS.EMAIL.CLIENT_ID, client_secret=cls.SETTINGS.EMAIL.CLIENT_SECRET
            )
            cls.logger.info(f"[Environment] Email - Google {Environment.SETTINGS.EMAIL.USER} - Connection prepared")
        else:
            cls.logger.info("[Environment] Email - Environment prepared without Email connection")

    @classmethod
    def __prepare_s3_storage(cls):
        if cls.SETTINGS.S3.USE:
            s3 = S3StorageService()
            s3.init_connection(
                access_id=cls.SETTINGS.S3.ACCESS_ID,
                access_key=cls.SETTINGS.S3.ACCESS_KEY,
                service_name=cls.SETTINGS.S3.SERVICE_NAME,
                region_name=cls.SETTINGS.S3.REGION_NAME,
                bucket_name=cls.SETTINGS.S3.BUCKET_NAME,
            )
            cls.logger.info(f"[Environment] S3 - Bucket {Environment.SETTINGS.S3.BUCKET_NAME} connected")
            cls.STORAGE = s3
            cls.logger.info("[Environment] S3 - Storage prepared")
        else:
            cls.logger.info("[Environment] S3 - Environment prepared without S3 connection")
