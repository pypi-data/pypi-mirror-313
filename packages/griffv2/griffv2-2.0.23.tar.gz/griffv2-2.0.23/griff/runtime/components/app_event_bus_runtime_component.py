from typing import Type

from injector import Injector, Binder, singleton

from griff.appli.app_event.app_event_bus import AppEventBus
from griff.appli.event.event_middleware import EventMiddleware
from griff.appli.message.message_bus import ListMiddlewares
from griff.infra.registry.meta_registry import MetaAppEventHandlerRegistry
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
    import_handlers,
)
from griff.settings.griff_settings import GriffSettings


class AppEventBusRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(
        self, settings: GriffSettings, middlewares: list[Type[EventMiddleware]]
    ):
        self._settings = settings
        self._middlewares = middlewares

    def configure(self, binder: Binder) -> None:
        binder.bind(AppEventBus, to=AppEventBus, scope=singleton)

    def initialize(self, injector: Injector):
        app_event_bus = injector.get(AppEventBus)
        middlewares: ListMiddlewares = [injector.get(m) for m in self._middlewares]
        for context in self._settings.bounded_contexts:
            import_handlers(
                self._settings.project_dir,
                self._settings.get_app_event_handlers_path(context),
            )

        handlers = [injector.get(h) for h in MetaAppEventHandlerRegistry.list_types()]
        app_event_bus.initialize(handlers, middlewares)

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass
