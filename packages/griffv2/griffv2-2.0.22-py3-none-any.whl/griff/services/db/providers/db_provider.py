import abc
from contextlib import asynccontextmanager
from typing import List, TypeVar, Generic, Dict, Any

C = TypeVar("C")

DbRow = Dict[str, Any]


class DbProvider(Generic[C], abc.ABC):
    @abc.abstractmethod
    async def start(self) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def stop(self) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def get_connection(self) -> C:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def close_connection(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def execute(
        self, connection: C, sql: str | List[str]
    ) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def fetch_one(self, connection: C, sql: str) -> DbRow:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def fetch_all(
        self, connection: C, sql: str
    ) -> List[DbRow]:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def start_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def commit_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def rollback_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod  # type: ignore
    @asynccontextmanager
    async def transaction(self, connection: C):  # pragma: no cover
        ...
