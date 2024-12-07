from abc import ABC
from typing import TypeVar, Generic

from griff.domain.common_types import TenantEntity, EntityId, TenantId
from griff.infra.repository.base_repository import BaseRepository

A = TypeVar("A", bound=TenantEntity)


# noinspection PyMethodOverriding
class TenantRepository(Generic[A], BaseRepository[A], ABC):
    async def get_by_id(self, entity_id: EntityId, tenant_id: TenantId) -> A | None:
        return await self._check_by_id(entity_id=entity_id, tenant_id=tenant_id)

    async def list_all(self, tenant_id: TenantId) -> list[A]:
        return await self._list_all(tenant_id=tenant_id)

    async def run_query(self, query_name: str, tenant_id: TenantId, **query_params):
        query_params["tenant_id"] = tenant_id
        return await self._run_query(query_name=query_name, **query_params)

    async def check_by_aggregate(self, aggregate: A) -> A | None:
        return await self.get_by_id(
            entity_id=aggregate.entity_id, tenant_id=aggregate.tenant_id
        )

    async def _get_persistence_by_aggregate(self, aggregate: A) -> dict | None:
        return await self._get_persistence_by_id(
            entity_id=aggregate.entity_id, tenant_id=aggregate.tenant_id
        )
