from injector import Injector

from griff.runtime.components.db_test_in_transaction_component import (
    DbTestInTransactionRuntimeComponent,
)
from griff.settings.griff_settings import GriffSettings
from griff.utils.db_tpl_utils import DbTplUtils


class DbTestContextInTransactionRuntimeComponent(DbTestInTransactionRuntimeComponent):
    def __init__(self, context: str, settings: GriffSettings):
        self._context = context
        self._settings = settings
        self._db_tpl = DbTplUtils(context=context, settings=settings)

    async def async_start(self, injector: Injector):
        await self._db_tpl.load()
        await super().async_start(injector)

    async def async_stop(self, injector: Injector):
        await super().async_stop(injector)
        await self._db_tpl.clean()
