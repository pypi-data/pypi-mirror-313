from griff.domain.common_types import DTO
from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.uniqid_service import UniqIdService

from {{ cookiecutter.context | snake_case }}._common.domain.{{ cookiecutter.aggregate | snake_case }} import {{cookiecutter.aggregate | pascal_case}}, Base{{cookiecutter.aggregate | pascal_case}}

# todo : à renommer
class Action{{cookiecutter.aggregate | pascal_case}}(Base{{cookiecutter.aggregate | pascal_case}}, DTO):
    ...

def {{ cookiecutter.command | snake_case }}({{ cookiecutter.aggregate | snake_case }}_action: Action{{cookiecutter.aggregate | pascal_case}}) -> {{cookiecutter.aggregate | pascal_case}}:
    entity_id = ServiceLocator.get(UniqIdService).get()
    return {{cookiecutter.aggregate | pascal_case}}(entity_id=entity_id, **{{ cookiecutter.aggregate | snake_case }}_action.model_dump())
