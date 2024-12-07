from abc import ABC
from dataclasses import dataclass
from typing import Type, Any

from griff.infra.registry.endpoint_decorator_processor import (
    EndpointDecoratorProcessor,
)
from griff.infra.registry.meta_registry import AbstractMetaRegistry
from griff.utils.inspect_utils import get_decorators


@dataclass
class EndpointDefinition:
    endpoint: Any
    http_method: str
    http_route: str
    http_success_code: int


class MetaEndpointControllerRegistry(AbstractMetaRegistry):
    ENDPOINT_REGISTRY: dict = {}

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        if ABC in bases:
            return new_cls

        for key, val in attrs.items():
            if key not in [
                "__module__",
                "__qualname__",
                "base_route",
                "router",
                "__classcell__",
                "__init__",
            ]:
                deco_list = get_decorators(val)

                if deco_list is None or len(deco_list) == 0:
                    continue

                decorator_processor = EndpointDecoratorProcessor()
                decorator_processor.load_decorators(deco_list)

                if decorator_processor.route is None:
                    # decorator is not an endpoint decorator
                    continue

                endpoint_def = EndpointDefinition(
                    endpoint=str(val).split(".")[1].split(" ")[0],
                    http_method=decorator_processor.method,
                    http_route=decorator_processor.route,
                    http_success_code=decorator_processor.code,
                )
                mcs.add_endpoint_to_controller(
                    endpoint=endpoint_def, controller=new_cls
                )

        return new_cls

    @classmethod
    def add_endpoint_to_controller(mcs, endpoint: EndpointDefinition, controller: Type):
        if controller not in mcs.ENDPOINT_REGISTRY.keys():
            mcs.ENDPOINT_REGISTRY[controller] = list()

        if endpoint.http_route in [
            e.http_route for e in mcs.ENDPOINT_REGISTRY[controller]
        ]:
            raise ValueError(
                f"route {endpoint.http_route} already registered "
                f"for {controller.__name__}"
            )

        mcs.ENDPOINT_REGISTRY[controller].append(endpoint)

    @classmethod
    def get_endpoint_registry(mcs):
        return mcs.ENDPOINT_REGISTRY

    @classmethod
    def get_full_route_for_endpoint(cls, controller, endpoint: EndpointDefinition):
        base_route = controller.base_route.strip("/") if controller.base_route else ""
        endpoint_route = endpoint.http_route.strip("/")
        if base_route == "":
            return f"/{endpoint_route.strip('/')}"
        fullroute = f"/{base_route}/{endpoint_route}"
        return fullroute
