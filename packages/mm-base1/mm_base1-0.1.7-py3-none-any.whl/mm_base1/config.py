from __future__ import annotations

import importlib.metadata

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _get_package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return " unknown"


class BaseAppConfig(BaseSettings):
    app_name: str
    data_dir: str
    access_token: str
    domain: str
    database_url: str
    database_tz_aware: bool = True
    debug: bool = False
    mm_b1_version: str = _get_package_version("mm-base1")
    app_version: str = _get_package_version("app")

    tags: list[str] = Field(default_factory=list)
    main_menu: dict[str, str] = Field(default_factory=dict)
    telegram_bot_help: str = "update me!"

    use_https: bool = True

    @property
    def tags_metadata(self) -> list[dict[str, str]]:
        base = [
            {"name": "dconfig"},
            {"name": "dvalue"},
            {"name": "dlog"},
            {"name": "system"},
            {"name": "auth"},
            {"name": "base-ui"},
        ]
        app = [{"name": t} for t in self.tags]
        return app + base

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
