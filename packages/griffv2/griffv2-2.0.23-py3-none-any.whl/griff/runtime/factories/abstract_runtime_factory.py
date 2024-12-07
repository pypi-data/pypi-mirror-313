import sys
from abc import ABC
from typing import Self, Type, TypeVar, Generic, Any

from loguru import logger

from griff.appli.app_event.middlewares.app_event_logger_middleware import (
    AppEventLoggerMiddleware,
)
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.command.middlewares.command_event_dispatch_middleware import (
    CommandEventDispatchMiddleware,
)
from griff.appli.command.middlewares.command_logger_middleware import (
    CommandLoggerMiddleware,
)
from griff.appli.command.middlewares.command_uow_middleware import CommandUowMiddleware
from griff.appli.event.event_middleware import EventMiddleware
from griff.appli.event.middlewares.event_logger_middleware import EventLoggerMiddleware
from griff.appli.query.middlewares.query_logger_middleware import QueryLoggerMiddleware
from griff.appli.query.query_middleware import QueryMiddleware
from griff.context_entry_point import ContextEntryPoint, AR, CR
from griff.runtime.components.abstract_runtime_component import RuntimeComponent
from griff.runtime.components.app_event_bus_runtime_component import (
    AppEventBusRuntimeComponent,
)
from griff.runtime.components.command_bus_runtime_component import (
    CommandBusRuntimeComponent,
)
from griff.runtime.components.common_cli_runtime_component import (
    CommonCliRuntimeComponent,
)
from griff.runtime.components.context_api_runtime_component import (
    ContextApiRuntimeComponent,
)
from griff.runtime.components.context_cli_runtime_component import (
    ContextCliRuntimeComponent,
)
from griff.runtime.components.db_runtime_component import DbRuntimeComponent
from griff.runtime.components.default_services_runtime_component import (
    DefaultServicesRuntimeComponent,
)
from griff.runtime.components.event_bus_runtime_component import (
    EventBusRuntimeComponent,
)
from griff.runtime.components.fastapi_runtime_component import FastApiRuntimeComponent
from griff.runtime.components.inject_runtime_component import (
    InjectRuntimeComponent,
    Injectable,
)
from griff.runtime.components.query_bus_runtime_component import (
    QueryBusRuntimeComponent,
)
from griff.runtime.components.service_locator_runtime_component import (
    ServiceLocatorRuntimeComponent,
)
from griff.runtime.runtime import Runtime
from griff.services.date.date_service import DateService
from griff.services.uniqid.uniqid_service import UniqIdService
from griff.settings.griff_settings import GriffSettings, LogLevel

S = TypeVar("S", bound=GriffSettings)
Injectables = dict[Type[Any], Injectable]


class AbstractRuntimeFactory(Generic[S], ABC):  # pragma: no cover
    def __init__(self, settings: S | None = None) -> None:
        self._settings = settings
        self._components: list[RuntimeComponent] = []
        self.with_injectable(GriffSettings, self._settings)

    def build(self) -> Runtime[S]:
        return self._build()

    def with_injectable(self, klass: Type[Any], to: Injectable) -> Self:
        self._add_component(InjectRuntimeComponent(klass, to))
        return self

    def with_default_services(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(DefaultServicesRuntimeComponent(self._settings))
        return self

    def with_service_locator(self) -> Self:
        self._add_component(
            ServiceLocatorRuntimeComponent([UniqIdService, DateService])
        )
        return self

    def with_injectables(self, injectables: Injectables) -> Self:
        for klass, to in injectables.items():
            self.with_injectable(klass, to)
        return self

    def with_db(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(DbRuntimeComponent(self._settings))
        return self

    def with_log_level(self, log_level: LogLevel | None = None) -> Self:
        logger.remove()
        default_log_level = (
            LogLevel.INFO.value
            if self._settings is None
            else self._settings.log_level.value
        )
        level = default_log_level if log_level is None else log_level
        logger.add(sys.stderr, level=level)
        return self

    def with_command_bus(self, for_cli: bool = False) -> Self:
        middlewares = (
            self._cli_command_bus_middlewares()
            if for_cli
            else self._command_bus_middlewares()
        )
        self._add_component(CommandBusRuntimeComponent(middlewares))
        return self

    def with_event_bus(self, for_cli: bool = False) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        middlewares = (
            self._cli_event_bus_middlewares()
            if for_cli
            else self._event_bus_middlewares()
        )
        self._add_component(EventBusRuntimeComponent(self._settings, middlewares))
        return self

    def with_app_event_bus(self, for_cli: bool = False) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        middlewares = (
            self._cli_app_event_bus_middlewares()
            if for_cli
            else self._app_event_bus_middlewares()
        )
        self._add_component(AppEventBusRuntimeComponent(self._settings, middlewares))
        return self

    def with_query_bus(self, for_cli: bool = False) -> Self:
        middlewares = (
            self._cli_query_bus_middlewares()
            if for_cli
            else self._query_bus_middlewares()
        )
        self._add_component(QueryBusRuntimeComponent(middlewares))
        return self

    def with_fastapi(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(FastApiRuntimeComponent(self._settings))
        return self

    def with_context_api(
        self, context_entry_point_class: Type[ContextEntryPoint[AR, CR]]
    ) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(ContextApiRuntimeComponent(context_entry_point_class))
        return self

    def with_common_cli(self) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(CommonCliRuntimeComponent())
        return self

    def with_context_cli(
        self, context_entry_point_class: Type[ContextEntryPoint[AR, CR]]
    ) -> Self:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        self._add_component(ContextCliRuntimeComponent(context_entry_point_class))
        return self

    def _add_component(self, component: RuntimeComponent) -> Self:
        self._components.append(component)
        return self

    def _build(self) -> Runtime[S]:
        if self._settings is None:
            # to avoid mypy error settings can be None
            raise self._settings_missing_exception()
        return Runtime(self._settings, self._components)

    # noinspection PyMethodMayBeStatic
    def _command_bus_middlewares(self) -> list[Type[CommandMiddleware]]:
        return [
            CommandLoggerMiddleware,
            CommandUowMiddleware,
            CommandEventDispatchMiddleware,
        ]

    # noinspection PyMethodMayBeStatic
    def _event_bus_middlewares(self) -> list[Type[EventMiddleware]]:
        return [EventLoggerMiddleware]

    # noinspection PyMethodMayBeStatic
    def _app_event_bus_middlewares(self) -> list[Type[EventMiddleware]]:
        return [AppEventLoggerMiddleware]

    # noinspection PyMethodMayBeStatic
    def _query_bus_middlewares(self) -> list[Type[QueryMiddleware]]:
        return [QueryLoggerMiddleware]

    def _cli_command_bus_middlewares(self) -> list[Type[CommandMiddleware]]:
        return self._command_bus_middlewares()

    def _cli_event_bus_middlewares(self) -> list[Type[EventMiddleware]]:
        return self._event_bus_middlewares()

    def _cli_app_event_bus_middlewares(self) -> list[Type[EventMiddleware]]:
        return self._app_event_bus_middlewares()

    def _cli_query_bus_middlewares(self) -> list[Type[QueryMiddleware]]:
        return self._query_bus_middlewares()

    @staticmethod
    def _settings_missing_exception() -> RuntimeError:
        return RuntimeError("Settings are missing, call with_settings before with_db")
