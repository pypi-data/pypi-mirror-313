from typing import List, TypeVar, Generic

from fastapi import FastAPI
from injector import Injector
from typer import Typer

from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    InjectBindable,
    Runnable,
    AsyncRunnable,
)
from griff.settings.griff_settings import GriffSettings

S = TypeVar("S", bound=GriffSettings)


class Runtime(Generic[S]):
    def __init__(
        self,
        settings: S,
        components: List[RuntimeComponent],
    ) -> None:
        self._settings = settings
        self._components = components
        self._injector = Injector(self._inject_bindable_components)

    def initialize(self):
        for component in self._runnable_components:
            component.initialize(self._injector)

    def clean(self):
        for component in self._runnable_components:
            component.clean(self._injector)

    def start(self):
        for component in self._runnable_components:
            component.start(self._injector)

    def stop(self):
        for component in self._runnable_components:
            component.stop(self._injector)

    async def async_start(self):
        for component in self._async_runnable_components:
            await component.async_start(self._injector)

    async def async_stop(self):
        for component in self._async_runnable_components:
            await component.async_stop(self._injector)

    def get_injector(self) -> Injector:
        return self._injector

    def get_settings(self) -> S:
        return self._settings

    def get_cli(self) -> Typer:  # pragma: no cover
        return self._injector.get(Typer)

    def get_fastapi_app(self) -> FastAPI:  # pragma: no cover
        app = self._injector.get(FastAPI)
        app.add_event_handler("startup", self.async_start)
        app.add_event_handler("shutdown", self.async_stop)
        return app

    @property
    def _runnable_components(self):
        return [c for c in self._components if isinstance(c, Runnable)]

    @property
    def _async_runnable_components(self):
        return [c for c in self._components if isinstance(c, AsyncRunnable)]

    @property
    def _inject_bindable_components(self):
        return [c.configure for c in self._components if isinstance(c, InjectBindable)]
