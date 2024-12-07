import os
from typing import Tuple, Type, TypeVar

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


def env_file() -> tuple[str, ...]:
    envs = ()
    env = os.getenv("WEBA_ENV", "dev")

    match env:
        case "production" | "prod" | "prd":
            envs = (".env", ".env.local", ".env.prd", ".env.prod", ".env.production")
        case "staging" | "stg":
            envs = (".env", ".env.local", ".env.stg", ".env.staging")
        case "testing" | "test" | "tst":
            envs = (".env", ".env.local", ".env.tst", ".env.test", ".env.testing")
        case _:
            envs = (".env", ".env.local", ".env.dev", ".env.development")

    return envs


class WebaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="weba_",
        env_file=env_file(),
        extra="ignore",
        env_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],  # noqa: ARG003
        init_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        env_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )

    env: str = "dev"

    debug: bool = False

    node_dev_cmd: list[str] = ["npm", "run", "dev"]

    script_dev_url_prefix: str = "http://127.0.0.1:5173"
    """Default is Vite"""

    ui_attrs_to_dash: bool = True

    html_parser: str = "html.parser"
    xml_parser: str = "xml"

    @property
    def is_test(self) -> bool:
        return self.env in ("test", "testing", "tst")

    @property
    def is_tst(self) -> bool:
        return self.env in ("test", "testing", "tst")

    @property
    def is_dev(self) -> bool:
        return self.env in ("dev", "development", "dev")

    @property
    def is_stg(self) -> bool:
        return self.env in ("staging", "stg")

    @property
    def is_prd(self) -> bool:
        return self.env in ("production", "prod", "prd")

    @property
    def environment(self) -> str:
        env = None

        match self.env:
            case "production" | "prod" | "prd":
                env = "production"
            case "staging" | "stg":
                env = "staging"
            case "testing" | "test" | "tst":
                env = "testing"
            case _:
                env = "development"

        return env


env = WebaSettings()

T = TypeVar("T", bound="WebaSettings")


def load_settings(settings_cls: Type[T], env_prefix: str = "app_") -> T:
    weba_env_keys = set(WebaSettings.__annotations__.keys())
    settings_keys = set(settings_cls.__annotations__.keys())
    weba_envs = {k: v for k, v in env.model_dump().items() if k in weba_env_keys - settings_keys}
    weba_envs["_env_prefix"] = env_prefix

    return settings_cls(**weba_envs)
