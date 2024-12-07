from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.event.event_handler import EventHandler
from griff.infra.persistence.persistence import Persistence
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase

CH = TypeVar("CH", bound=EventHandler)


class EventHandlerTestCase(Generic[CH], RuntimeTestMixin, TestCase, ABC):
    handler: CH

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
    def handler_class(self) -> Type[CH]:
        pass
