from typing import Type

from injector import Injector, Binder, singleton

from griff.appli.message.message_bus import ListMiddlewares
from griff.appli.query.middlewares.query_logger_middleware import QueryLoggerMiddleware
from griff.appli.query.query_bus import QueryBus
from griff.appli.query.query_middleware import QueryMiddleware
from griff.infra.registry.meta_registry import (
    MetaQueryHandlerRegistry,
)
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
)


class QueryBusRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(self, middlewares: list[Type[QueryMiddleware]]):
        self._middlewares = middlewares

    def configure(self, binder: Binder) -> None:
        binder.bind(QueryBus, to=QueryBus, scope=singleton)

    def initialize(self, injector: Injector):
        query_bus = injector.get(QueryBus)
        middlewares: ListMiddlewares = [injector.get(m) for m in self._middlewares]
        handlers = [injector.get(h) for h in MetaQueryHandlerRegistry.list_types()]
        query_bus.initialize(handlers, middlewares)

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass

    @staticmethod
    def _list_middlewares() -> list[Type[QueryMiddleware]]:
        return [QueryLoggerMiddleware]
