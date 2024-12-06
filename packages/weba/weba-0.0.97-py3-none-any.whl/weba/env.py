import os

from pydantic_settings import (
    BaseSettings,
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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="weba_",
        env_file=env_file(),
        extra="ignore",
        env_file_encoding="utf-8",
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


env = Settings()
