from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from griff.infra.api.api_router import ApiRouter
from griff.infra.cli.cli_router import CliRouter
from griff.infra.registry.meta_registry import MetaContextEntryPointRegistry

AR = TypeVar("AR", bound=ApiRouter)
CR = TypeVar("CR", bound=CliRouter)


class ContextEntryPoint(Generic[AR, CR], ABC, metaclass=MetaContextEntryPointRegistry):
    @abstractmethod
    def __init__(self, api_router: AR | None = None, cli_router: CR | None = None):
        self._api_router = api_router
        self._cli_router = cli_router

    def get_api_router(self) -> AR | None:  # pragma: no cover
        return self._api_router

    def get_cli_router(self) -> CR | None:  # pragma: no cover
        return self._cli_router

    @staticmethod
    @abstractmethod
    def context_name() -> str:  # pragma: no cover
        ...
