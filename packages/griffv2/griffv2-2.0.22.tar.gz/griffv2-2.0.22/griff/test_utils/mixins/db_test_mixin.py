from abc import ABC

from asyncpg import Connection

from griff.runtime.runtime import Runtime
from griff.services.db.providers.asyncpg_provider import AsyncPgProvider
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory


class DbTestMixin(RuntimeTestMixin, ABC):
    provider: AsyncPgProvider
    runtime: Runtime

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().test_with_db()

    @classmethod
    def setup_class(cls):
        if hasattr(super(), "setup_class"):
            super().setup_class()
        cls.async_to_sync(cls.create_test_db)

    @classmethod
    def teardown_class(cls):
        if hasattr(super(), "teardown_class"):
            super().teardown_class()
        cls.async_to_sync(cls.drop_test_db)

    @classmethod
    async def create_test_db(cls):
        provider = cls._get_template1_provider()
        async with provider.connection() as conn:
            try:
                await cls._create_test_db(provider, conn)
            except Exception:
                # gestion d'un test qui aurait échoué et qui n'aurait pas fait sont
                # teardown
                await cls._disconnect_all(provider, conn)
                await cls._drop_test_db(provider, conn)
                await cls._create_test_db(provider, conn)

    @classmethod
    async def drop_test_db(cls):
        provider = cls._get_template1_provider()
        async with provider.connection() as conn:
            try:
                await cls._drop_test_db(provider, conn)
            except Exception as e:
                print(f"ERROR: {e}")

    @classmethod
    async def _create_test_db(cls, provider: AsyncPgProvider, conn: Connection):
        # noinspection SqlInjection
        sql = f"CREATE DATABASE {cls.runtime.get_settings().db.name}"
        await provider.execute(conn, sql)

    @classmethod
    async def _drop_test_db(cls, provider: AsyncPgProvider, conn: Connection):
        # noinspection SqlInjection
        sql = f"DROP DATABASE {cls.runtime.get_settings().db.name}"
        await provider.execute(conn, sql)

    @classmethod
    def _get_template1_provider(cls):
        settings = cls.runtime.get_settings().db.copy(deep=True)
        settings.name = "template1"
        return AsyncPgProvider(settings)

    @classmethod
    async def _disconnect_all(cls, provider: AsyncPgProvider, conn: Connection):
        # noinspection SqlInjection
        await cls._get_nb_active_connexion(provider, conn)
        await provider.disconnect_all(conn)

    @classmethod
    async def _get_nb_active_connexion(
        cls, provider: AsyncPgProvider, conn: Connection
    ):
        row = await provider.fetch_one(
            conn, "SELECT sum(numbackends) as nb FROM pg_stat_database;"
        )
        print(f"{row['nb']} connexion active")
        return row["nb"]
