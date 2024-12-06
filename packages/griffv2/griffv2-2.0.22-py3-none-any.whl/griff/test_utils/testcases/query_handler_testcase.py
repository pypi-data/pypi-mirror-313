from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.query.query_handler import QueryHandler, QueryResponse
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase

QH = TypeVar("QH", bound=QueryHandler)


class QueryHandlerTestCase(Generic[QH], RuntimeTestMixin, TestCase, ABC):
    handler: QH

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().command_test_handler()

    def setup_method(self):
        super().setup_method()
        self.handler = self.get_injected(self.handler_class)

    @staticmethod
    def prepare_success_resultset(response: QueryResponse):
        return response.model_dump()

    @property
    @abstractmethod
    def handler_class(self) -> Type[QH]:
        pass
