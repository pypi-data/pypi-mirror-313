from pydantic import Field
from pydantic_settings import BaseSettings


class DbPoolSettings(BaseSettings):
    min_size: int = 10
    max_size: int = 50


class DbSettings(BaseSettings):
    name: str
    host: str
    port: int = 5432
    user: str
    password: str
    pool: DbPoolSettings = Field(default_factory=DbPoolSettings)

    @property
    def dsn(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @property
    def driver(self) -> str:
        return "asyncpg"

    @property
    def db_test_name(self) -> str:  # pragma: no cover
        return f"test_{self.name}"
