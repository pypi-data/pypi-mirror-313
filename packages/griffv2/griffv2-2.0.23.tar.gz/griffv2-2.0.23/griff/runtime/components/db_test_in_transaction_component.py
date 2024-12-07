from injector import Binder, Injector

from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    InjectBindable,
    AsyncRunnable,
)
from griff.services.db.db_service import DbService
from griff.services.db.db_test_service import DbTestService
from griff.utils.async_utils import AsyncUtils


class DbTestInTransactionRuntimeComponent(
    AsyncUtils, InjectBindable, AsyncRunnable, RuntimeComponent
):
    """Seulement à usage des tests unitaires"""

    def configure(self, binder: Binder) -> None:
        binder.bind(DbService, DbTestService)

    async def async_init(self, injector: Injector):
        pass

    async def async_shutdown(self, injector: Injector):
        pass

    async def async_start(self, injector: Injector):
        db_service = injector.get(DbService)
        await db_service.start_transaction()

    async def async_stop(self, injector: Injector):
        db_service = injector.get(DbService)
        await db_service.rollback_transaction()
