from typing import Self, TypeVar, Generic, Type

from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.command.middlewares.command_event_dispatch_middleware import (
    CommandEventDispatchMiddleware,
)
from griff.appli.event.event_middleware import EventMiddleware
from griff.appli.query.query_middleware import QueryMiddleware
from griff.context_entry_point import ContextEntryPoint
from griff.runtime.components.db_runtime_component import DbTestRuntimeComponent
from griff.runtime.components.db_test_context_in_transaction_runtime_component import (
    DbTestContextInTransactionRuntimeComponent,
)
from griff.runtime.components.db_test_in_transaction_component import (
    DbTestInTransactionRuntimeComponent,
)
from griff.runtime.components.default_services_runtime_component import (
    DefaultServicesTestRuntimeComponent,
)
from griff.runtime.components.fake_persistence_test_context_runtime_component import (
    FakePersistenceTestContextRuntimeComponent,
)
from griff.runtime.factories.abstract_runtime_factory import (
    AbstractRuntimeFactory,
    Injectables,
)
from griff.settings.pytest_settings import PytestSettings

S = TypeVar("S", bound=PytestSettings)


class PytestRuntimeFactory(Generic[S], AbstractRuntimeFactory[S]):  # pragma: no cover
    def base_test(self) -> Self:
        self.with_log_level().with_default_services().with_service_locator()
        return self

    def test_with_db(self) -> Self:
        return self.base_test().with_db_test()

    def domain_test(self) -> Self:
        return self.base_test()

    def repository_test(
        self, context_entry_point_class: Type[ContextEntryPoint]
    ) -> Self:
        return self.test_with_db().with_context_in_db_transaction(
            context_entry_point_class.context_name()
        )

    def persistence_test(
        self, context_entry_point_class: Type[ContextEntryPoint]
    ) -> Self:
        return self.test_with_db().with_context_in_db_transaction(
            context_entry_point_class.context_name()
        )

    def api_test(self, context_entry_point_class: Type[ContextEntryPoint]) -> Self:
        return (
            self.test_with_db()
            .with_context_in_db_transaction(context_entry_point_class.context_name())
            .with_command_bus()
            .with_event_bus()
            .with_query_bus()
            .with_fastapi()
            .with_context_api(context_entry_point_class)
        )

    def cli_test(self, context_entry_point_class: Type[ContextEntryPoint]) -> Self:
        return (
            self.test_with_db()
            .with_context_in_db_transaction(context_entry_point_class.context_name())
            .with_command_bus(for_cli=True)
            .with_event_bus(for_cli=True)
            .with_query_bus(for_cli=True)
            .with_context_api(context_entry_point_class)
        )

    def command_test_handler(self) -> Self:
        return self.base_test()

    def event_test_handler(self) -> Self:
        return self.base_test()

    def with_default_services(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(DefaultServicesTestRuntimeComponent(self._settings))
        return self

    def with_injectables(self, injectables: Injectables | None = None) -> Self:
        if injectables is None:
            return self
        return super().with_injectables(injectables)

    def with_db_test(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(DbTestRuntimeComponent(self._settings))
        return self

    def with_test_in_db_transaction(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(DbTestInTransactionRuntimeComponent())
        return self

    def with_context_in_db_transaction(self, context_name: str) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(
            DbTestContextInTransactionRuntimeComponent(context_name, self._settings)
        )
        return self

    def with_context_fake_persistence(self, context_name: str) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(
            FakePersistenceTestContextRuntimeComponent(context_name, self._settings)
        )
        return self

    def _command_bus_middlewares(self) -> list[Type[CommandMiddleware]]:
        return [CommandEventDispatchMiddleware]

    # noinspection PyMethodMayBeStatic
    def _event_bus_middlewares(self) -> list[Type[EventMiddleware]]:
        return []

    # noinspection PyMethodMayBeStatic
    def _query_bus_middlewares(self) -> list[Type[QueryMiddleware]]:
        return []
