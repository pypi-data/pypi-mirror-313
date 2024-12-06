import typing
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Optional, Union, Type
from urllib.parse import urlencode

import httpx
import orjson
from fastapi import FastAPI
from fastapi import Response, status
from pydantic import BaseModel, Field, field_validator, model_validator

from griff.appli.event.event_handler import FakeEventHandler
from griff.context_entry_point import ContextEntryPoint
from griff.infra.persistence.persistence import QueryRowResults
from griff.infra.repository.repository import Repository
from griff.services.json.json_service import JsonService
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase


class ApiClientParams(BaseModel):
    data_json: Optional[Union[list, dict]] = Field(None, alias="json")
    data: Optional[Union[list, dict]] = Field(None, alias="data")
    files: Optional[dict] = None
    auto_auth: bool = True
    access_token: Optional[str] = None
    headers: Optional[dict] = None

    @model_validator(mode="after")
    def check_auto_auth(cls, values):
        if values.auto_auth and values.access_token is None:
            raise ValueError("Missing Jwt Access Token for automatic authentication")
        return values

    @field_validator("headers")
    @classmethod
    def set_header(cls, value):
        return value or {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.auto_auth:
            self.headers["Authorization"] = f"Bearer {self.access_token}"
        self._json_service = JsonService()

    def to_method_kwargs(self) -> dict:
        kwargs = super().dict(
            exclude={"auto_auth", "access_token"}, by_alias=True, exclude_none=True
        )
        if "json" in kwargs:
            kwargs["json"] = self._json_service.to_json_dumpable(kwargs["json"])
        if "data" in kwargs:
            kwargs["data"] = self._json_service.to_json_dumpable(kwargs["data"])
        return kwargs


# noinspection PyMethodOverriding
class FastApiTestClient(httpx.AsyncClient):
    default_access_token: str | None = None

    @typing.no_type_check
    async def post(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        data: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = True,
        access_token=None,
        headers: dict | None = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            data=data,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().post(url=url, **params)

    @typing.no_type_check
    async def get(
        self,
        url,
        auto_auth: bool = True,
        access_token=None,
        headers: dict | None = None,
    ) -> Response:
        params = ApiClientParams(
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().get(url=url, **params)

    @typing.no_type_check
    async def put(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = True,
        access_token=None,
        headers: dict | None = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().put(url=url, **params)

    @typing.no_type_check
    async def patch(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = True,
        access_token=None,
        headers: dict | None = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        )
        return await super().patch(url=url, **params.to_method_kwargs())

    @typing.no_type_check
    async def delete(
        self,
        url,
        auto_auth: bool = True,
        access_token=None,
        headers: dict | None = None,
    ) -> Response:
        params = ApiClientParams(
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().delete(url=url, **params)


class ApiTestCase(RuntimeTestMixin, TestCase, ABC):
    app: FastAPI
    client: FastApiTestClient

    @classmethod
    @abstractmethod
    def entry_point_class(cls) -> Type[ContextEntryPoint]:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().api_test(cls.entry_point_class())

    def setup_method(self):
        super().setup_method()
        self.app = self.get_injected(FastAPI)
        self.client = FastApiTestClient(app=self.app, base_url="http://test")

    def assert_response_equals_resultset(
        self, response: Response, remove_paths: Optional[list] = None
    ):
        return self.assert_equals_resultset(
            self.prepare_response_for_resultset(response), remove_paths=remove_paths
        )

    def assert_response_status_code(
        self, response: Response, status=status.HTTP_200_OK
    ):
        assert status == response.status_code, (
            f"expected status {status} got {response.status_code}\n"
            f"response body: {self.get_response_body(response)}"
        )

    @classmethod
    def prepare_response_for_resultset(cls, response: Response):
        try:
            return {
                "status_code": response.status_code,
                "body": cls.get_response_body(response),
            }
        except Exception as e:
            pprint(cls.get_response_body(response))
            raise e

    @typing.no_type_check
    def list_api_routes(self, api_name, except_routes: list | None = None):
        if except_routes is None:
            except_routes = []
        return [
            route
            for route in self.app.routes
            if f"{api_name}:" in route.name and route.name not in except_routes
        ]

    def reverse_url(self, name, query_kwargs=None, **kwargs):
        """
        Url reverse from FastAPI routes

        Usage:
            reverse(
                <url_name>,
                pk=123,
                query_kwargs={'key':'value', 'k2': 'v2'}
            )
            => url/123?key=value&k2=v2

        Args:
            name: route name
            query_kwargs: optional query params
            **kwargs: route url params

        Returns:
            str: relative url built from router name and params with query params
            if asked
        """
        base_url = self.app.url_path_for(name, **kwargs)
        if query_kwargs:
            return f"{base_url}?{urlencode(query_kwargs, doseq=True)}"

        return base_url

    @classmethod
    def get_response_body(cls, response: Response):
        content = response.content  # type: ignore
        return orjson.loads(content) if content else None

    async def prepare_success_resultset(
        self,
        response: Response,
        repository: Repository,
        event_handler: FakeEventHandler,
    ):
        results: QueryRowResults = await repository._persistence.list_all()
        return {
            "response": self.prepare_response_for_resultset(response),
            "persistence": results,
            "handled_events": event_handler.list_events_handled(),
        }
