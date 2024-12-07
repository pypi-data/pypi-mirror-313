from typing import TypeVar

from injector import Binder, Injector

from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    InjectBindable,
    AsyncRunnable,
)
from griff.services.db.db_service import DbService
from griff.services.db.db_settings import DbSettings
from griff.services.db.providers.asyncpg_provider import AsyncPgProvider
from griff.services.db.providers.db_provider import DbProvider
from griff.settings.griff_settings import GriffSettings

S = TypeVar("S", bound=GriffSettings)


class DbRuntimeComponent(AsyncRunnable, InjectBindable, RuntimeComponent):
    def __init__(self, settings: S):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(DbSettings, self._settings.db)
        binder.bind(DbProvider, AsyncPgProvider)  # type: ignore

    async def async_start(self, injector: Injector):
        db_service = injector.get(DbService)
        await db_service.start()

    async def async_stop(self, injector: Injector):
        db_service = injector.get(DbService)
        await db_service.stop()


class DbTestRuntimeComponent(InjectBindable, RuntimeComponent):
    def __init__(self, settings: S):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(DbSettings, self._settings.db)
        binder.bind(DbProvider, AsyncPgProvider)  # type: ignore
