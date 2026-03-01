from pydantic_settings import SettingsConfigDict

from config.environs.base import EnvironSettings


class EnvironSettingsProd(EnvironSettings):
    model_config = SettingsConfigDict(env_file=".env.prod")

    ENV: str = "PROD"
