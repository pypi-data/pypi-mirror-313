import random
from abc import ABC
from decimal import Decimal
from typing import Self, List, Dict, Optional, Any

from griff.domain.common_types import Entity
from griff.infra.persistence.persistence import Persistence
from griff.infra.repository.repository import Repository
from griff.services.date.fake_date_service import FakeDateService
from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.uniqid_service import UniqIdService


class DataTestFactory(ABC):
    def __init__(self, start_id: int = 1):
        self.uniqid_service = ServiceLocator.get(UniqIdService)
        self.date_service = FakeDateService()
        self._repositories: Dict[str, Repository] = {}
        self._sequence: Dict = {}
        self._created: Dict = {}
        random.seed(42)
        self._random_state = random.getstate()
        self.reset(start_id)

    async def persist(
        self, repository: Repository, data: list[Entity] | Entity
    ) -> Self:
        if isinstance(data, list) is False:
            await repository.save(data)
            return self

        for a in data:
            await repository.save(a)
        return self

    async def persist_by_persistence(
        self, persistence: Persistence, data: List[Entity] | Entity
    ) -> Self:
        initial_data = data if isinstance(data, list) else [data]
        prepared_data = [d.model_dump() for d in initial_data]
        persistence.reset(initial_data=prepared_data)
        return self

    def random_decimal(self, min, max) -> Decimal:
        random.setstate(self._random_state)
        min = float(min) * 100
        max = float(max) * 100
        val = Decimal(random.uniform(min, max)) / 100
        self._random_state = random.getstate()
        return val

    def random_int(self, min, max) -> int:
        random.setstate(self._random_state)
        val = random.randrange(min, max)
        self._random_state = random.getstate()
        return val

    def random_existing_asset(self, asset_type: str) -> Any:
        return random.choice(self._created[asset_type])

    def next_sequence(self, name: str) -> int:
        if name not in self._sequence:
            self._sequence[name] = 0
        self._sequence[name] += 1
        return self._sequence[name]

    def current_sequence(self, name: str) -> int:
        return self._sequence[name]

    def list_created(self, name):
        return self._created[name] if name in self._created else []

    def reset_sequence_id(self, start: int = 1) -> Self:
        self.uniqid_service.reset(start)
        return self

    def reset(self, start_id=1) -> Self:
        self.reset_sequence_id(start_id)
        for repository in self._repositories.values():
            if repository:
                repository.reset()
        return self

    async def persist_created(
        self, name: str, data: Optional[list[Entity] | Entity] = None
    ) -> Self:
        if self._has_repository(name) is False:
            raise RuntimeError(f"Repository {name} not found")
        data = data if data else self._created[name]
        return await self.persist(self._repositories[name], data)

    async def persist_all_created(self):
        """
        !! les données seront persistées dans l'ordre de création de chaque type
        de données créées
        """
        for name, created in self._created.items():
            if self._has_repository(name) is False:
                continue
            await self.persist_created(name, created)
        return self

    def _add_created(self, name, created):
        if name not in self._created:
            self._created[name] = []
        self._created[name].append(created)
        return created

    def _has_repository(self, name: str) -> bool:
        return name in self._repositories and self._repositories[name] is not None
