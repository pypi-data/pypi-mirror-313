from abc import ABC
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

EntityId = Annotated[str, Field(max_length=36, min_length=26, frozen=True)]


class DTO(BaseModel, ABC):
    ...


class ValueObject(BaseModel, ABC):
    model_config = ConfigDict(
        use_enum_values=True, validate_default=True, extra="forbid", frozen=True
    )


class Entity(BaseModel, ABC):
    model_config = ConfigDict(use_enum_values=True, validate_default=True, frozen=True)
    entity_id: EntityId

    @classmethod
    def classname(cls) -> str:  # pragma: no cover
        return str(cls)

    @classmethod
    def short_classname(cls) -> str:
        return cls.__name__

    @classmethod
    def _entity_label(cls) -> str:
        return cls.short_classname()


# noinspection Pydantic
class Aggregate(Entity, ABC):
    pass


# Tenant
TenantId = EntityId


class TenantEntity(Entity, ABC):
    tenant_id: TenantId


class TenantAggregate(Aggregate, TenantEntity):
    ...
