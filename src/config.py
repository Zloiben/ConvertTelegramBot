from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'config',
)


class Config(BaseSettings):
    BOT_TOKEN: str
    CONVERT_SERVICE_TOKEN: str
    MODE: Literal["PROD", "TEST", "DEV"]

    model_config = SettingsConfigDict(env_file='.env')


config = Config()
