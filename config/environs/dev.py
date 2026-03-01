from pydantic_settings import SettingsConfigDict

from config.environs.base import EnvironSettings


class EnvironSettingsDev(EnvironSettings):
    model_config = SettingsConfigDict(env_file=".env.dev")

    ENV: str = "DEV"
