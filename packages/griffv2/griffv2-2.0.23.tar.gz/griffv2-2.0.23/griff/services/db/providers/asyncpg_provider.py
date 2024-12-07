import threading
from contextlib import asynccontextmanager
from typing import List

import asyncpg
from asyncpg import Pool, Connection
from asyncpg.transaction import Transaction
from injector import inject, singleton
from loguru import logger

from griff.services.db.db_settings import DbSettings
from griff.services.db.providers.db_provider import DbProvider, DbRow


@singleton
class AsyncPgProvider(DbProvider[Connection]):
    @inject
    def __init__(self, settings: DbSettings):
        self._settings = settings
        self._transactions: dict[int, Transaction] = {}
        self._pool: Pool | None = None
        self._debug = False

    async def start(self) -> None:
        if self._pool is None:
            self.debug("--->START POOL")
            self._pool = await asyncpg.create_pool(
                dsn=self._settings.dsn, **self._settings.pool.model_dump()
            )

    async def stop(self) -> None:
        if self._pool is not None:
            self.debug("--->STOP POOL")
            self._pool.terminate()
            self._pool = None

    async def get_connection(self) -> Connection:
        if self._pool:
            self.debug("--->GET CONNECTION FROM POOL")
            return await self._pool.acquire()
        self.debug("--->GET CONNECTION")
        return await asyncpg.connect(self._settings.dsn)

    async def close_connection(self, connection: Connection) -> None:
        if self._pool:
            self.debug(f"--->RELEASE POOL CONNECTION {id(connection)}")
            await self._pool.release(connection)
            return None
        self.debug(f"--->CLOSE CONNECTION {id(connection)}")
        await connection.close()

    @asynccontextmanager
    async def connection(self) -> Connection:
        connection = await self.get_connection()
        try:
            yield connection
        finally:
            await self.close_connection(connection)

    async def execute(self, connection: Connection, sql: str | List[str]) -> None:
        if isinstance(sql, list):
            sql = ";\n".join(sql)
        self.debug(f"--->execute {sql}")
        await connection.execute(sql)

    async def fetch_one(self, connection: Connection, sql: str) -> DbRow:
        self.debug(f"--->fetch_one {sql}")
        row = await connection.fetchrow(sql)
        return dict(row)

    async def fetch_all(self, connection: Connection, sql: str) -> List[DbRow]:
        self.debug(f"--->fetch_all {sql}")
        rows = await connection.fetch(sql)
        return [dict(row) for row in rows]

    async def start_transaction(self, connection: Connection) -> None:
        conn_id = self._get_connection_id(connection)
        if conn_id in self._transactions:
            raise RuntimeError(
                f"a transaction is already started for connection {conn_id}"
            )

        self._transactions[conn_id] = connection.transaction()
        await self._transactions[conn_id].start()

    async def commit_transaction(self, connection: Connection) -> None:
        conn_id = self._get_connection_id(connection)
        transaction = self._check_transaction_exists(conn_id)
        await transaction.commit()
        self._transactions.pop(conn_id)

    async def rollback_transaction(self, connection: Connection) -> None:
        conn_id = self._get_connection_id(connection)
        transaction = self._check_transaction_exists(conn_id)
        await transaction.rollback()
        self._transactions.pop(conn_id)

    @asynccontextmanager
    async def transaction(self, connection: Connection) -> Transaction:
        async with connection.transaction():
            yield

    async def disconnect_all(self, connection: Connection) -> None:
        # noinspection SqlInjection
        sql = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{self._settings.name}' "
            "AND pid <> pg_backend_pid();"
        )
        await connection.execute(sql)

    def _check_transaction_exists(self, conn_id: int) -> Transaction:
        if conn_id in self._transactions:
            return self._transactions[conn_id]
        raise RuntimeError(f"no transaction started for connection {conn_id}")

    @staticmethod
    def _get_connection_id(connection: Connection) -> int:
        return id(connection)

    def debug(self, msg: str) -> None:  # pragma: no cover
        if self._debug is True:
            logger.debug(f" PG : {threading.current_thread().ident} {msg}")
