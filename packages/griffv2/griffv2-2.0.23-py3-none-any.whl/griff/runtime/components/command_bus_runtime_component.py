from typing import Type, List, Any

from injector import Injector, Binder, singleton

from griff.appli.command.command_bus import CommandBus
from griff.appli.command.command_handler import CommandHandler
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.message.message_bus import ListMiddlewares
from griff.infra.registry.meta_registry import MetaCommandHandlerRegistry
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
)


class CommandBusRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(self, middlewares: list[Type[CommandMiddleware]]):
        self._middlewares = middlewares

    def configure(self, binder: Binder) -> None:
        binder.bind(CommandBus, to=CommandBus, scope=singleton)

    def initialize(self, injector: Injector) -> None:
        command_bus = injector.get(CommandBus)
        middlewares: ListMiddlewares = [injector.get(m) for m in self._middlewares]
        handlers: List[CommandHandler[Any, Any]] = [
            injector.get(h) for h in MetaCommandHandlerRegistry.list_types()
        ]
        command_bus.initialize(handlers, middlewares)

    def clean(self, injector: Injector) -> None:
        pass

    def start(self, injector: Injector) -> None:
        pass

    def stop(self, injector: Injector) -> None:
        pass
