from abc import abstractmethod, ABC
from typing import Type, Any

from griff.appli.event.event_handler import FakeEventHandler
from griff.context_entry_point import ContextEntryPoint
from griff.infra.repository.repository import Repository
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase
from griff.utils.async_utils import AsyncUtils


class CliTestCase(RuntimeTestMixin, TestCase, ABC):
    @classmethod
    @abstractmethod
    def entry_point_class(cls) -> Type[ContextEntryPoint]:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().cli_test(cls.entry_point_class())

    @staticmethod
    def prepare_success_resultset(
        repository: Repository, fake_event_handler: FakeEventHandler | None = None
    ):
        results = AsyncUtils.async_to_sync(repository._persistence.list_all)
        actual: dict[str, Any] = {"persistence": results}
        if fake_event_handler:
            actual["handled_events"] = fake_event_handler.list_events_handled()

        return actual
