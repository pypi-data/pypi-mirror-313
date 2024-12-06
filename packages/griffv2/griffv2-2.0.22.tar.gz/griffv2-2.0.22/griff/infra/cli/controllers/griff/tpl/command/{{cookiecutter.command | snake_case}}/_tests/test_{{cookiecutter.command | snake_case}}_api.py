import pytest
from typing import Type

from griff.appli.event.event_bus import EventBus
from griff.appli.event.event_handler import FakeEventHandler
from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.testcases.api_testcase import ApiTestCase, FastApiTestClient
from injector import singleton

from access._common.test_utils.mixins.access_test_mixin import AccessTestMixin
from {{ cookiecutter.context | snake_case }}.entry_point import {{ cookiecutter.context | pascal_case }}EntryPoint
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_event import {{ cookiecutter.CommandEvent }}
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import {{cookiecutter.aggregate | pascal_case}}Repository
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf
from {{ cookiecutter.context | snake_case }}._common.api.{{ cookiecutter.context | snake_case }}_schemas import {{ cookiecutter.command | pascal_case }}In

@singleton
class FakeOn{{ cookiecutter.CommandEvent }}Handler(FakeEventHandler):
    on_event_type = {{ cookiecutter.CommandEvent }}

@pytest.mark.skip(reason="not yet implemented")
class Test{{ cookiecutter.command | pascal_case }}Api(AccessTestMixin, ApiTestCase):
    @classmethod
    def entry_point_class(cls) -> Type[{{ cookiecutter.context | pascal_case }}EntryPoint]:
        return {{ cookiecutter.context | pascal_case }}EntryPoint

    @classmethod
    def with_injectables(cls) -> Injectables | None:
        return super().with_injectables()

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.dtf = {{ cookiecutter.context | pascal_case }}Dtf(start_id=99990)
        cls.event_bus = cls.get_injected(EventBus)
        cls.event_handler = cls.get_injected(FakeOn{{ cookiecutter.CommandEvent }}Handler)
        cls.repository = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Repository)
        {{ cookiecutter.aggregate | snake_case }} = cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}()
        cls.api_in = {{ cookiecutter.command | pascal_case }}In(**{{ cookiecutter.aggregate | snake_case }}.model_dump())
        # hack temporaire le temps de trouver comment se passer de AccessTestMixin
        FastApiTestClient.default_access_token = cls.get_access_token(
            cls.active_account
        )

    def setup_method(self):
        super().setup_method()
        self.dtf.reset(1)

    """
    POST /{{ cookiecutter.context | snake_case }}/{{ cookiecutter.command | snake_case }}
    """

    async def test_{{ cookiecutter.command | snake_case }}_avec_donnees_obligatoires_manquante_echoue(self):
        response = await self.client.post(self.reverse_url("{{ cookiecutter.command | snake_case }}"), json={})
        self.assert_response_equals_resultset(response)

    async def test_{{ cookiecutter.command | snake_case }}_reussi(self):
        response = await self.client.post(self.reverse_url("{{ cookiecutter.command | snake_case }}"), json=self.api_in.model_dump())
        self.assert_equals_resultset(
            await self.prepare_success_resultset(response, self.repository, self.event_handler)
        )

    async def test_{{ cookiecutter.command | snake_case }}_composante_pour_chaque_permission(self):
        actual = await self.assert_pour_chaque_permission(
            method="post",
            url=self.reverse_url("{{ cookiecutter.command | snake_case }}"),
            json=self.api_in.model_dump(),
        )
        self.assert_equals_resultset(actual)
