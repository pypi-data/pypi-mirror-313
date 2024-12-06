from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from injector import inject

from griff.domain.common_types import Entity, TenantEntity
from griff.infra.persistence.serialized_persistence import SerializedPersistence
from griff.infra.repository.repository import Repository
from griff.infra.repository.tenant_repository import TenantRepository
from griff.services.date.date_service import DateService

A = TypeVar("A", bound=Entity)
TA = TypeVar("TA", bound=TenantEntity)


class SerializedRepository(Generic[A], Repository[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: SerializedPersistence,
        date_service: DateService,
    ):
        super().__init__(persistence, date_service)


class SerializedTenantRepository(Generic[TA], TenantRepository[TA], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: SerializedPersistence,
        date_service: DateService,
    ):
        persistence.add_excluded_field("tenant_id")
        super().__init__(persistence, date_service)
