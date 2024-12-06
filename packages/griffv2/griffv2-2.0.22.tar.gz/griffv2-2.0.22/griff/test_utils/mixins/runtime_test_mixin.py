import abc
from typing import TypeVar, Type

from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.runtime.runtime import Runtime
from griff.services.uniqid.uniqid_service import UniqIdService
from griff.test_utils.mixins.async_test_mixin import AsyncTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory

K = TypeVar("K")


class RuntimeTestMixin(AsyncTestMixin, abc.ABC):
    runtime: Runtime
    uniqid_service: UniqIdService
    _pytest_runtime_factory: PytestRuntimeFactory  # must be set in conftest.py

    @classmethod
    def setup_class(cls):
        cls.runtime = (
            cls.runtime_factory().with_injectables(cls.with_injectables()).build()
        )
        cls.uniqid_service = cls.get_injected(UniqIdService)
        cls.runtime.initialize()
        if hasattr(super(), "setup_class"):
            super().setup_class()

    @classmethod
    def teardown_class(cls):
        cls.runtime.clean()
        if hasattr(super(), "teardown_class"):
            super().teardown_class()

    def setup_method(self):
        self.runtime.start()
        if hasattr(super(), "setup_method"):
            super().setup_method()

    def teardown_method(self):
        if hasattr(super(), "teardown_method"):
            super().teardown_method()
        self.runtime.stop()

    async def async_setup(self):
        await self.runtime.async_start()

    async def async_teardown(self):
        await self.runtime.async_stop()

    @classmethod
    @abc.abstractmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return cls._runtime_factory()

    @classmethod
    @abc.abstractmethod
    def with_injectables(cls) -> Injectables | None:
        pass

    @classmethod
    def get_injected(cls, klass: Type[K]) -> K:
        return cls.runtime.get_injector().get(klass)

    @classmethod
    def get_settings(cls):
        return cls.runtime.get_settings()

    @classmethod
    def _runtime_factory(cls) -> PytestRuntimeFactory:
        if not hasattr(cls, "_pytest_runtime_factory"):
            raise AttributeError(
                "cls._pytest_runtime_factory must be set in conftest.py"
            )
        return cls._pytest_runtime_factory
