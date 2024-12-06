from typing import Type

from injector import Injector
from loguru import logger
from typer import Typer

from griff.context_entry_point import ContextEntryPoint
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
)


class ContextCliRuntimeComponent(Runnable, RuntimeComponent):
    def __init__(self, context_entry_point_class: Type[ContextEntryPoint]):
        self._entry_point_class = context_entry_point_class

    def initialize(self, injector: Injector):
        entry_point = injector.get(self._entry_point_class)
        context_router = entry_point.get_cli_router()
        if context_router is None:
            logger.warning("No CLI router found for entry point {self._entry_point}")
            return None
        typer = injector.get(Typer)
        typer.add_typer(
            context_router.get_app(), name=context_router.get_command_group_name()
        )

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass
