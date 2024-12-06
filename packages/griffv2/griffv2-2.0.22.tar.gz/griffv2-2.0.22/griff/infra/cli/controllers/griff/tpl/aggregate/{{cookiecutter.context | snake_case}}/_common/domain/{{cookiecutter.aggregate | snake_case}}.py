from abc import ABC
from typing import TypeAlias
from griff.domain.common_types import Aggregate, EntityId
from pydantic import BaseModel

{{cookiecutter.aggregate | pascal_case}}Id: TypeAlias = EntityId


class Base{{cookiecutter.aggregate | pascal_case}}(BaseModel, ABC):
    ...

class {{cookiecutter.aggregate | pascal_case}}(Base{{cookiecutter.aggregate | pascal_case}}, Aggregate):
    entity_id: {{cookiecutter.aggregate | pascal_case}}Id
