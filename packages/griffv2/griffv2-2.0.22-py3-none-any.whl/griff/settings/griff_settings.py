import enum
from abc import ABC
from pathlib import Path
from typing import Set

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from griff.services.db.db_settings import DbSettings
from griff.services.jwt.jwt_settings import JwtSettings
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings


class LogLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LocaleSettings(BaseSettings):
    default: str
    relative_path: str = "app/locale"
    pydantic_locale_dir_name: str = "pydantic"
    fastapi_locale_dir_name: str = "fastapi"


class CORSSettings(BaseSettings):
    allow_origins: Set[str] = {"localhost"}
    allow_credentials: bool = True
    allow_methods: Set[str] = {"*"}
    allow_headers: Set[str] = {"*"}

    # @field_validator("allow_origins", "allow_methods", "allow_headers", mode="before")
    # @classmethod
    # def str_to_set(cls, v) :
    #     return v


class GriffSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        validate_assignment=True,
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    env: str = "prod"

    project_name: str
    project_dir: str
    bounded_contexts: list[str] = Field(default_factory=list)

    debug: bool = False
    log_level: LogLevel = LogLevel.INFO

    db: DbSettings
    cors: CORSSettings = Field(default_factory=CORSSettings)

    locale: LocaleSettings | None = None

    jwt: JwtSettings | None = None
    query_runner: QueryRunnerSettings | None = None

    @model_validator(mode="after")
    def set_query_runner_dir(self):
        if self.query_runner is None:
            self.query_runner = QueryRunnerSettings(
                project_dir=self.project_dir, driver=self.db.driver
            )
        if self.query_runner.project_dir is None:
            self.query_runner.project_dir = self.project_dir
        return self

    @property
    def full_locale_path(self):
        locale = self._check_locale()
        return str(Path(self.project_dir).joinpath(locale.relative_path))

    @property
    def pydantic_locale_path(self) -> str:
        locale = self._check_locale()
        return str(
            Path(self.project_dir).joinpath(
                locale.relative_path, locale.pydantic_locale_dir_name
            )
        )

    @property
    def fastapi_local_path(self) -> str:
        locale = self._check_locale()
        return str(
            Path(self.project_dir).joinpath(
                locale.relative_path, locale.fastapi_locale_dir_name
            )
        )

    def get_app_path(self, absolute: bool = True) -> Path:
        base_path = Path(self.project_dir) if absolute else Path("./")
        return base_path.joinpath("app")

    def get_app_event_handlers_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_context_path(context, absolute).joinpath("app_event_handlers")

    def get_context_path(self, context: str, absolute: bool = True) -> Path:
        if context not in self.bounded_contexts:
            raise ValueError(f"Context {context} is not in bounded contexts")

        base_path = Path(self.project_dir) if absolute else Path("./")
        return base_path.joinpath(context)

    def get_event_handlers_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_context_path(context, absolute).joinpath("event_handlers")

    def get_common_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_context_path(context, absolute).joinpath("_common")

    def get_repositories_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_common_path(context, absolute).joinpath("repositories")

    def get_migrations_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_repositories_path(context, absolute).joinpath("migrations")

    def get_queries_path(self, context: str, domain: str, absolute: bool = True):
        return self.get_repositories_path(context, absolute).joinpath(domain, "sql")

    def get_test_utils_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_common_path(context, absolute).joinpath("test_utils")

    def _check_locale(self) -> LocaleSettings:
        if self.locale is None:
            raise ValueError("Locale settings are not set")
        return self.locale
