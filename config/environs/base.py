from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironSettingsBase(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding="utf-8", extra="ignore")


class EnvironSettingsDirectories(EnvironSettingsBase):
    LOGS: Optional[str] = None
    LOCAL_STORAGE: Optional[str] = None
    FILE_STORAGE: Optional[str] = None


class EnvironSettingsDatabase(EnvironSettingsBase):
    ENGINE: Optional[str] = None
    NAME: Optional[str] = None
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None
    HOST: Optional[str] = None
    PORT: Optional[str] = None

    def get_db_url(self):
        return f"{self.ENGINE}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class EnvironSettingsTokenEmail(EnvironSettingsBase):
    USE: Optional[bool] = False
    USER: Optional[str] = None
    CLIENT_ID: Optional[str] = None
    CLIENT_SECRET: Optional[str] = None
    SEND_EMAILS: Optional[bool] = False


class EnvironSettingsRedis(EnvironSettingsBase):
    USE: Optional[bool] = False
    HOST: Optional[str] = None
    PORT: Optional[str] = None
    USER: Optional[str] = ""
    PASSWORD: Optional[str] = False
    SSL: Optional[bool] = False

    def get_url(self):
        redis_protocol = "rediss" if self.SSL else "redis"
        redis_user_pass = f":{self.PASSWORD}"
        url = f"{redis_protocol}://{redis_user_pass}@{self.HOST}:{self.PORT}"
        return url


class EnvironSettingsS3(EnvironSettingsBase):
    USE: Optional[bool] = False
    ACCESS_ID: str = None
    ACCESS_KEY: str = None
    SERVICE_NAME: str = None
    REGION_NAME: str = None
    BUCKET_NAME: str = None


class EnvironSettingsSentry(EnvironSettingsBase):
    USE: Optional[bool] = False
    DSN: Optional[str] = None
    USE_PII: Optional[bool] = False
    SEND_DEFAULT_PII: Optional[bool] = False
    USE_TRACING: Optional[bool] = False
    TRACES_SAMPLE_RATE: Optional[float] = 0
    USE_PROFILING: Optional[bool] = False
    PROFILE_SESSION_SAMPLE_RATE: Optional[float] = 0
    PROFILE_LIFECYCLE: Optional[str] = "trace"


class EnvironSettingsIA(EnvironSettingsBase):
    OPENAI_API_KEY: Optional[str] = None


class EnvironSettingsAudit(EnvironSettingsBase):
    USE: Optional[bool] = False
    SAVE_IP_ON_FAIL: Optional[bool] = False


class EnvironSettings(EnvironSettingsBase):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    ENV: str
    APP_NAME: str
    SECRET_KEY: str
    DEBUG: bool
    DIRECTORY: EnvironSettingsDirectories
    FRONTEND_URL: str
    TOKEN_EXPIRED_AFTER_SECONDS: int

    # BACK
    DB: Optional[EnvironSettingsDatabase] = None
    AUDIT: Optional[EnvironSettingsAudit] = None

    # Optional
    SENTRY: Optional[EnvironSettingsSentry] = None
    EMAIL: Optional[EnvironSettingsTokenEmail] = None
    S3: Optional[EnvironSettingsS3] = None
    REDIS: Optional[EnvironSettingsRedis] = None
    IA: Optional[EnvironSettingsIA] = None
