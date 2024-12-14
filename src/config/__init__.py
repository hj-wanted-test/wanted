import os
from os import environ, path

from pydantic_settings import BaseSettings, SettingsConfigDict

root_path = _root_path = path.realpath(path.join(path.dirname(__file__), ".."))

ENV = os.environ.get("APP_ENV", "LOCAL").lower()

_config_path = path.join(root_path, "config")
ENV_FILES = [path.join(_config_path, "base.env")]
_env_file = path.join(_config_path, f"{ENV}.env")
if path.exists(_env_file):
    ENV_FILES.append(_env_file)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILES, env_file_encoding="utf-8")

    ENV: str
    DEBUG: bool

    APP_NAME: str
    DB_URL: str


conf = Settings()
