from typing import Callable

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from dishka import Scope, Provider, make_container


class LaunchConfig(BaseModel):
    app: str
    host: str
    port: int
    reload: bool
    workers: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__"
    )
    conf: LaunchConfig


def get_settings() -> Settings:
    return Settings()


def get_provider() -> Provider:
    return Provider()


def scope_provider(provider: Provider, func: Callable, scope: Scope):
    provider.provide(func, scope=scope)






