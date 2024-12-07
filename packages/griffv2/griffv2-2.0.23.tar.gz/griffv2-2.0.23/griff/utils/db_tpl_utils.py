from pathlib import Path

import asyncpg

from griff.services.db.providers.asyncpg_provider import AsyncPgProvider
from griff.settings.griff_settings import GriffSettings
from griff.utils.migration_utils import MigrationUtils


# noinspection SqlInjection
class DbTplUtils:  # pragma: no cover
    def __init__(
        self,
        context: str,
        settings: GriffSettings,
    ):
        self.context = context
        self.settings = settings
        name = self.settings.project_name.replace(" ", "_").lower()
        self.tpl_db_name = f"test_{name}_{self.context}"
        self._db_tpl_settings = self.settings.db.model_copy(
            update={"name": self.tpl_db_name}, deep=True
        )
        self.default_db_name = self.settings.db.name
        self._template1_provider = self._get_template1_provider()
        self._db_tpl_provider = self._get_db_tpl_provider()

    @property
    def db_tpl_path(self) -> Path:
        return self.settings.get_test_utils_path(self.context).joinpath("db_tpl")

    @property
    def migrations_path(self) -> Path:
        return self.settings.get_migrations_path(self.context)

    @property
    def dump_filename(self) -> Path:
        return self.db_tpl_path.joinpath("db_tpl.dump")

    @property
    def dump_sql_filename(self) -> Path:
        return self.db_tpl_path.joinpath("db_tpl.sql")

    async def create(self) -> None:
        async with self._template1_provider.connection() as conn:
            await self._template1_provider.execute(conn, self._create_sql)

    async def delete(self) -> None:
        async with self._template1_provider.connection() as conn:
            await self._delete(conn)

    async def is_db_exists(self) -> bool:
        try:
            conn = await self._db_tpl_provider.get_connection()
        except asyncpg.InvalidCatalogNameError:
            return False
        await conn.close()
        return True

    async def recreate(self) -> None:
        async with self._template1_provider.connection() as conn:
            await self._delete(conn)
            await self._template1_provider.execute(conn, self._create_sql)

    async def load(self) -> None:
        async with self._template1_provider.connection() as conn:
            # noinspection PyBroadException
            try:
                await self._template1_provider.execute(conn, self._clone_db_sql)
            except Exception:
                await self._template1_provider.execute(conn, self._delete_cloned_sql)
                await self._template1_provider.execute(conn, self._clone_db_sql)

    async def clean(self) -> None:
        async with self._template1_provider.connection() as conn:
            await self._template1_provider.execute(conn, self._delete_cloned_sql)

    def is_context_exists(self) -> bool:
        context_path = self.settings.get_context_path(self.context)
        return context_path.exists()

    async def restore_from_sql(self) -> None:
        if self.dump_sql_filename.exists() is False:
            raise RuntimeError(f"no dump sql found for context {self.context}")
        with open(str(self.dump_sql_filename)) as f:
            sql = f.read()

        await self.recreate()

        async with self._db_tpl_provider.connection() as conn:
            await self._db_tpl_provider.execute(conn, sql)

    def do_migration(self) -> None:
        if self.migrations_path.exists() is False:
            raise RuntimeError(f"Migration path for context '{self.context}' not found")
        MigrationUtils.migrate(self._db_tpl_settings.dsn, str(self.migrations_path))

    async def _delete(self, conn) -> None:
        await self._template1_provider.disconnect_all(conn)
        # drop table must be executed alone
        await self._template1_provider.execute(conn, self._delete_sql)

    def _get_template1_provider(self) -> AsyncPgProvider:
        settings = self.settings.db.model_copy(update={"name": "template1"}, deep=True)
        return AsyncPgProvider(settings)

    def _get_db_tpl_provider(self) -> AsyncPgProvider:
        return AsyncPgProvider(self._db_tpl_settings)

    @property
    def _initial_data_path(self) -> Path:
        return self.db_tpl_path.joinpath("initial_db_tpl_data.py")

    @property
    def _create_sql(self) -> str:
        return f"CREATE DATABASE {self.tpl_db_name}"

    @property
    def _delete_sql(self) -> str:
        return f"DROP DATABASE IF EXISTS {self.tpl_db_name}"

    @property
    def _clone_db_sql(self) -> str:
        return f"CREATE DATABASE {self.default_db_name} TEMPLATE {self.tpl_db_name}"

    @property
    def _delete_cloned_sql(self) -> str:
        return f"DROP DATABASE {self.default_db_name}"
