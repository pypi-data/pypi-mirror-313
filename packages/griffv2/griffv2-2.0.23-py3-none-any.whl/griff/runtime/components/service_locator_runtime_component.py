from typing import TypeVar, List, Type

from injector import Injector

from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
)
from griff.services.abstract_service import AbstractService
from griff.services.service_locator.service_locator import ServiceLocator
from griff.settings.griff_settings import GriffSettings

S = TypeVar("S", bound=GriffSettings)


class ServiceLocatorRuntimeComponent(Runnable, RuntimeComponent):
    def __init__(self, services: List[Type[AbstractService]]):
        self._services = services

    def initialize(self, injector: Injector):
        ServiceLocator.reset()
        for service in self._services:
            ServiceLocator.register(service, injector.get(service))

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass

    def clean(self, injector: Injector):
        ServiceLocator.reset()
