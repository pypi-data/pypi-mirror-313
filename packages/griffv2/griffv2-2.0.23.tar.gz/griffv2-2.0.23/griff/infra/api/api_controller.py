from abc import ABC
from typing import Any

from starlette.responses import JSONResponse

from griff.appli.message.message_handler import (
    MessageSuccessResponse,
    MessageErrorResponse,
)
from griff.appli.message.message_middleware import MessageContext
from griff.infra.registry.meta_endpoint_controller_registry import (
    MetaEndpointControllerRegistry,
)
from griff.utils.inspect_utils import find_bound_method_to_object


class ApiController(ABC, metaclass=MetaEndpointControllerRegistry):
    def __init__(self) -> None:
        """
        Auto register endpoint in fastApi router
        """
        endpoint_list = MetaEndpointControllerRegistry.get_endpoint_registry()[
            type(self)
        ]
        self._endpoints = list()
        for endpoint in endpoint_list:
            endpoint_route = MetaEndpointControllerRegistry.get_full_route_for_endpoint(
                controller=self, endpoint=endpoint
            )
            if endpoint_route is None:  # pragma: no cover
                continue
            self._endpoints.append(
                {
                    "route": endpoint_route,
                    "method": endpoint.http_method,
                    "func": find_bound_method_to_object(self, endpoint.endpoint),
                    "return_code": endpoint.http_success_code,
                }
            )

    def get_endpoints(self) -> list[dict[str, Any]]:
        return self._endpoints

    @staticmethod
    def prepare_response(
        response: MessageSuccessResponse | MessageErrorResponse,
    ) -> Any | JSONResponse:  # pragma: no cover
        if response.is_success:
            return response.content

        return JSONResponse(status_code=response.code, content=response.dump_content())

    @staticmethod
    def _get_token_context(token: str) -> MessageContext:  # pragma: no cover
        return MessageContext(context={"access_token": token})
