from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.app_event.app_event_handler import AppEventHandler
from griff.infra.persistence.persistence import Persistence
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase

AEH = TypeVar("AEH", bound=AppEventHandler)


class AppEventHandlerTestCase(Generic[AEH], RuntimeTestMixin, TestCase, ABC):
    handler: AEH

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().event_test_handler()

    def setup_method(self):
        super().setup_method()
        self.handler = self.get_injected(self.handler_class)

    @staticmethod
    async def prepare_success_resultset(persistence: Persistence):
        return {"persistence": await persistence.list_all()}

    @property
    @abstractmethod
    def handler_class(self) -> Type[AEH]:
        pass
