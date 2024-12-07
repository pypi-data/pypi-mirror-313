from typing import Type

import pytest
import typer
from griff.appli.event.event_handler import FakeEventHandler
from injector import singleton
from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.testcases.cli_testcase import CliTestCase
from griff.utils.async_utils import AsyncUtils

from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import {{cookiecutter.aggregate | pascal_case}}Repository
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf
from params.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_cli import {{cookiecutter.command | pascal_case}}CliController
from {{ cookiecutter.context | snake_case }}.entry_point import {{ cookiecutter.context | pascal_case }}EntryPoint
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_event import {{ cookiecutter.CommandEvent }}

@singleton
class FakeOn{{ cookiecutter.CommandEvent }}Handler(FakeEventHandler):
    on_event_type = {{ cookiecutter.CommandEvent }}

class Test{{ cookiecutter.command | pascal_case }}Cli(CliTestCase):
    @classmethod
    def entry_point_class(cls) -> Type[{{ cookiecutter.context | pascal_case }}EntryPoint]:
        return {{ cookiecutter.context | pascal_case }}EntryPoint

    @classmethod
    def with_injectables(cls) -> Injectables | None:
        return {}

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.dtf = cls.get_injected({{cookiecutter.context | pascal_case}}Dtf)
        cls.dtf.reset_sequence_id(99990)
        cls.repository = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Repository)
        cls.event_handler = cls.get_injected(FakeOn{{ cookiecutter.CommandEvent }}Handler)
        cls.existing_{{ cookiecutter.aggregate | snake_case }} = cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}()

    def setup_method(self):
        super().setup_method()
        self.controller = self.get_injected({{cookiecutter.command | pascal_case}}CliController)
        self.dtf.reset(1)

    async def async_setup(self):
        await super().async_setup()
        self.repository.reset()
        await self.dtf.persist_created("{{cookiecutter.aggregate | snake_case}}")

    """
    action
    """

    def test_{{ cookiecutter.command | snake_case }}_avec_un_pb_a_definir_echoue(self, capsys):
        match = "Echec action : Une erreur"
        with pytest.raises(typer.Exit):
            self.controller.action(
                **self.existing_{{ cookiecutter.aggregate | snake_case }}.model_dump(exclude={"entity_id"})
            )
        assert capsys.readouterr().out == f"{match}\n"

    def test_{{ cookiecutter.command | snake_case }}_reussi(self):
        assert self.controller.action(**self.existing_{{ cookiecutter.aggregate | snake_case }}.model_dump(exclude={"entity_id"})) is None
        self.assert_equals_resultset(
            {
                "db": AsyncUtils.async_to_sync(self.repository.run_query, "list_all"),
                "handled_events": self.event_handler.list_events_handled(),
            }
        )
