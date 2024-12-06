from typing import Type

from injector import inject

from griff.infra.repository.repository import Repository, FakeRepositoryMixin
from griff.services.date.date_service import DateService
from griff.infra.repository.serialized_repository import SerializedRepository

from {{ cookiecutter.context | snake_case }}._common.domain.{{ cookiecutter.aggregate | snake_case }} import {{cookiecutter.aggregate | pascal_case}}
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_persistence import {{cookiecutter.aggregate | pascal_case}}Persistence

class {{cookiecutter.aggregate | pascal_case}}Repository(SerializedRepository[{{cookiecutter.aggregate | pascal_case}}]):
    @inject
    def __init__(
        self, persistence: {{cookiecutter.aggregate | pascal_case}}Persistence,
        date_service: DateService
    ):
        super().__init__(persistence, date_service)

    @staticmethod
    def _aggregate_class(raw_data: dict | None = None) -> Type[{{cookiecutter.aggregate | pascal_case}}]:
        return {{cookiecutter.aggregate | pascal_case}}

######
# OU (supprimer l'implémentation inutile)
######
class {{cookiecutter.aggregate | pascal_case}}Repository(Repository[{{cookiecutter.aggregate | pascal_case}}]):
    @inject
    def __init__(
        self, persistence: {{cookiecutter.aggregate | pascal_case}}Persistence, date_service: DateService
    ):
        super().__init__(persistence, date_service)

    @staticmethod
    def _aggregate_class(raw_data: dict | None = None) -> Type[{{cookiecutter.aggregate | pascal_case}}]:  # pragma: no cover
        return {{cookiecutter.aggregate | pascal_case}}






class {{cookiecutter.aggregate | pascal_case}}FakeRepository(FakeRepositoryMixin, {{cookiecutter.aggregate | pascal_case}}Repository):
    ...
