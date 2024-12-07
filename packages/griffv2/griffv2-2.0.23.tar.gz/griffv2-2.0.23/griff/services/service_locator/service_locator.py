from typing import Dict, Type, TypeVar

from griff.services.abstract_service import AbstractService

S = TypeVar("S", bound=AbstractService)
ServiceContainer = Dict[str, S]


class ServiceLocator:
    _container: ServiceContainer = {}

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"{cls.__name__} can not be instantiated")

    @classmethod
    def register(cls, service_class: Type[S], service: S) -> None:
        container_key = cls._get_container_key(service_class)
        if container_key not in cls._container:
            cls._container[container_key] = service
            return None
        raise RuntimeError(f"{service.__class__.__name__} is already registered")

    @classmethod
    def get(cls, service_class: Type[S]) -> S:
        container_key = cls._get_container_key(service_class)
        if container_key in cls._container:
            return cls._container[container_key]
        raise RuntimeError(f"{service_class.__name__} is not registered")

    @classmethod
    def reset(cls):
        cls._container = {}

    @classmethod
    def _get_container_key(cls, service: Type[S]) -> str:
        return str(service)
