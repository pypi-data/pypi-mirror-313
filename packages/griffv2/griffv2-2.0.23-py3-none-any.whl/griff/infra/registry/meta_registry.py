from abc import ABC, ABCMeta
from typing import Type, Any, List


class AbstractMetaRegistry(ABCMeta, type):
    except_name = "None"
    REGISTRY: dict[str, Type[Any]]

    def __new__(cls, name: str, bases: Any, attrs: dict[str, Any]) -> Type[Any]:
        new_cls = type.__new__(cls, name, bases, attrs)
        if ABC in bases:
            # no need to register Abstract class
            return new_cls

        class_name = f"{new_cls.__module__}.{new_cls.__name__}"
        cls.REGISTRY[class_name] = new_cls
        return new_cls

    @classmethod
    def list_types(cls) -> List[Type[Any]]:
        return list(cls.REGISTRY.values())


class MetaQueryHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaEventHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaAppEventHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaCommandHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaContextEntryPointRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaApiRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaCliRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}
