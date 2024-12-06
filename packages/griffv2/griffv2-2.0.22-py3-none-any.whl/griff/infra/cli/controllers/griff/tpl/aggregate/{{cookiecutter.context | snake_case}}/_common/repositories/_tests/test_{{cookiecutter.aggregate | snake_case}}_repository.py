from typing import Type

from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.testcases.repository_testcase import RepositoryTestCase

from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import (
    {{cookiecutter.aggregate | pascal_case}}Repository,
)
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf
from {{ cookiecutter.context | snake_case }}.entry_point import {{ cookiecutter.context | pascal_case }}EntryPoint


class Test{{cookiecutter.aggregate | pascal_case}}Repository(RepositoryTestCase):
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
        cls.repository = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Repository)
        cls.{{ cookiecutter.aggregate | snake_case }}s = [
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
            cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}(),
        ]

    def setup_method(self):
        super().setup_method()

    """
    CRUD
    """

    async def test_crud_reussi(self) -> None:
        update_data = self.dtf.creer_{{ cookiecutter.aggregate | snake_case }}().model_dump(exclude={"entity_id"})
        self.assert_equals_resultset(
            await self.run_crud(
                repository=self.repository,
                aggregates=self.{{ cookiecutter.aggregate | snake_case }}s,
                aggregate_to_update=self.{{ cookiecutter.aggregate | snake_case }}s[1],
                update_data=update_data,
                aggregate_to_delete=self.{{ cookiecutter.aggregate | snake_case }}s[1],
            ),
        )
