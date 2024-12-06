from abc import ABC
from typing import TypeVar

from griff.domain.common_types import Entity
from griff.infra.persistence.dict_persistence import DictPersistence
from griff.infra.repository.base_repository import BaseRepository

A = TypeVar("A", bound=Entity)


class FakeRepositoryMixin:  # pragma: no cover
    _persistence: DictPersistence

    def reset(self):
        self._persistence.reset()


class Repository(BaseRepository[A], ABC):
    async def get_by_id(self, entity_id: str) -> A | None:
        return await self._check_by_id(entity_id=entity_id)

    async def list_all(self) -> list[A]:
        return await self._list_all()

    async def run_query(self, query_name: str, **query_params):
        return await self._run_query(query_name=query_name, **query_params)

    async def check_by_aggregate(self, aggregate: A) -> A | None:
        return await self.get_by_id(entity_id=aggregate.entity_id)

    async def _get_persistence_by_aggregate(self, aggregate: A) -> dict | None:
        return await self._get_persistence_by_id(entity_id=aggregate.entity_id)
