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
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None
    SSL: Optional[bool] = False

    def get_url(self):
        redis_protocol = "rediss" if self.SSL else "redis"
        auth = f"{self.USER or ''}:{self.PASSWORD or ''}@" if (self.USER or self.PASSWORD) else ""
        return f"{redis_protocol}://{auth}{self.HOST}:{self.PORT}"


class EnvironSettingsS3(EnvironSettingsBase):
    USE: Optional[bool] = False
    ACCESS_ID: Optional[str] = None
    ACCESS_KEY: Optional[str] = None
    SERVICE_NAME: Optional[str] = None
    REGION_NAME: Optional[str] = None
    BUCKET_NAME: Optional[str] = None


class EnvironSettingsSentry(EnvironSettingsBase):
    USE: Optional[bool] = False
    DSN: Optional[str] = None
    USE_PII: Optional[bool] = False
    SEND_DEFAULT_PII: Optional[bool] = False
    USE_TRACING: Optional[bool] = False
    TRACES_SAMPLE_RATE: Optional[float] = 0.0
    USE_PROFILING: Optional[bool] = False
    PROFILE_SESSION_SAMPLE_RATE: Optional[float] = 0.0
    PROFILE_LIFECYCLE: Optional[str] = "trace"


class EnvironSettingsIA(EnvironSettingsBase):
    OPENAI_API_KEY: Optional[str] = None


class EnvironSettingsAudit(EnvironSettingsBase):
    USE: Optional[bool] = False
    SAVE_IP_ON_FAIL: Optional[bool] = False


class EnvironSettingsApp(EnvironSettingsBase):
    NAME: str
    SECRET_KEY: str
    DEBUG: bool
    FRONTEND_URL: str
    TOKEN_EXPIRED_AFTER_SECONDS: int

    # Security (comma-separated values, e.g. "example.com,api.example.com")
    ALLOWED_HOSTS: Optional[str] = ""
    CORS_ALLOWED_ORIGINS: Optional[str] = ""

    # Request/response tracing middlewares
    LOG_REQUESTS: Optional[bool] = True
    LOG_RESPONSES: Optional[bool] = True

    def get_allowed_hosts(self) -> list[str]:
        return [host.strip() for host in (self.ALLOWED_HOSTS or "").split(",") if host.strip()]

    def get_cors_allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in (self.CORS_ALLOWED_ORIGINS or "").split(",") if origin.strip()]


class EnvironSettings(EnvironSettingsBase):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    ENV: str
    APP: EnvironSettingsApp
    DIRECTORY: EnvironSettingsDirectories

    # BACK
    DB: Optional[EnvironSettingsDatabase] = None
    AUDIT: Optional[EnvironSettingsAudit] = None

    # Optional
    SENTRY: Optional[EnvironSettingsSentry] = None
    EMAIL: Optional[EnvironSettingsTokenEmail] = None
    S3: Optional[EnvironSettingsS3] = None
    REDIS: Optional[EnvironSettingsRedis] = None
    IA: Optional[EnvironSettingsIA] = None
