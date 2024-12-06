from abc import ABC

from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase


class DomainTestCase(RuntimeTestMixin, TestCase, ABC):
    @classmethod
    def with_injectables(cls) -> Injectables | None:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().domain_test()
