import pytest
from typing import Type

from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.testcases.persistence_testcase import PersistenceTestCase

from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import {{cookiecutter.aggregate | pascal_case}}Repository
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_persistence import {{cookiecutter.aggregate | pascal_case}}Persistence
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf
from {{ cookiecutter.context | snake_case }}.entry_point import {{ cookiecutter.context | pascal_case }}EntryPoint


@pytest.mark.skip(reason="dès qu'il faut tester une requete")
class Test{{cookiecutter.aggregate | pascal_case}}Persistence(PersistenceTestCase):
    @classmethod
    def entry_point_class(cls) -> Type[{{ cookiecutter.context | pascal_case }}EntryPoint]:
        return {{ cookiecutter.context | pascal_case }}EntryPoint

    @classmethod
    def with_injectables(cls) -> Injectables | None:
        return {}

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.dtf = {{ cookiecutter.context | pascal_case }}Dtf()
        cls.persistence = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Persistence)
        cls.repository = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Repository)
        cls.{{ cookiecutter.aggregate | snake_case }}s = [
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
        ]

    def setup_method(self):
        super().setup_method()

    async def async_setup(self):
        await super().async_setup()
        await self.dtf.persist(self.repository, self.{{ cookiecutter.aggregate | snake_case }}s)

    """
    nom_requete
    """

    async def test_nom_requete_succes(self):
        actual = await self.persistence.run_query("nom_requete")
        self.assert_equals_resultset(actual)
