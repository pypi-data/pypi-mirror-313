from typing import Type

from fastapi import FastAPI
from injector import Injector
from loguru import logger

from griff.context_entry_point import ContextEntryPoint
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
)


class ContextApiRuntimeComponent(Runnable, RuntimeComponent):
    def __init__(self, context_entry_point_class: Type[ContextEntryPoint]):
        self._entry_point_class = context_entry_point_class

    def initialize(self, injector: Injector):
        entry_point = injector.get(self._entry_point_class)
        context_router = entry_point.get_api_router()
        if context_router is None:
            logger.warning("No API router found for entry point {self._entry_point}")
            return None
        app = injector.get(FastAPI)
        app.include_router(context_router.get_fastapi_router())

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass
