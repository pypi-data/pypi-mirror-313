from abc import ABC, abstractmethod
from typing import Callable, List

from fastapi import APIRouter

from griff.infra.api.api_controller import ApiController
from griff.infra.registry.meta_registry import MetaApiRouterRegistry


class ApiRouter(ABC, metaclass=MetaApiRouterRegistry):
    def __init__(self):
        self._router = APIRouter(prefix=self._route_prefix, tags=self._route_tags)
        for ctrl in self._list_controllers():
            for endpoint in ctrl.get_endpoints():
                self.add_endpoint(**endpoint)

    def get_fastapi_router(self) -> APIRouter:
        return self._router

    def add_endpoint(self, route: str, method: str, func: Callable, return_code: int):
        self._router.add_api_route(
            path=route, endpoint=func, methods=[method], status_code=return_code
        )

    @abstractmethod
    def _list_controllers(self) -> List[ApiController]:  # pragma: no cover
        ...

    @property
    @abstractmethod
    def _route_prefix(self) -> str:  # pragma: no cover
        pass

    @property
    @abstractmethod
    def _route_tags(self) -> List[str]:  # pragma: no cover
        pass
