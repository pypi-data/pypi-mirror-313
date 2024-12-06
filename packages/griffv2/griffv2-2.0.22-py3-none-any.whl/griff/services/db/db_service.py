import threading
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any

from injector import inject, singleton
from loguru import logger

from griff.services.abstract_service import AbstractService
from griff.services.db.providers.db_provider import (
    DbProvider,
)


@singleton
class DbService(AbstractService):
    @inject
    def __init__(self, provider: DbProvider):
        self._provider = provider
        self._current_connection = ContextVar("current_connection", default=None)
        self._debug = False

    async def start(self):
        self.debug("--->STARTING DB")
        await self._provider.start()

    async def stop(self):
        self.debug("--->CLOSING DB")
        await self._provider.stop()

    @asynccontextmanager
    async def connection(self):
        conn = self._get_current_connection()
        if conn is not None:
            self.debug(f"got TRANSACTION connection {id(conn)}")
            yield conn
        else:
            conn = await self._provider.get_connection()
            try:
                self.debug(f"got connection {id(conn)}")
                yield conn
            except Exception as e:
                raise e
            finally:
                self.debug(f"close connection {id(conn)}")
                await self._provider.close_connection(conn)

    @asynccontextmanager
    async def transaction(self):
        if self._get_current_connection() is not None:
            raise RuntimeError("A transaction is already running")

        conn = await self._provider.get_connection()
        token = self._set_current_connection(conn)
        self.debug(f"TRANSACTION START on {id(conn)}")
        try:
            async with self._provider.transaction(conn):
                yield conn
        finally:
            self.debug(f"release TRANSACTION connection {id(conn)}")
            await self._provider.close_connection(conn)
            self._reset_current_connection(token)

    async def start_transaction(self):
        if self._get_current_connection() is not None:
            raise RuntimeError("A transaction is already running")

        conn = await self._provider.get_connection()
        self.debug(f"TRANSACTION START on {id(conn)}")
        self._set_current_connection(conn)
        await self._provider.start_transaction(conn)

    async def commit_transaction(self):
        conn = self._get_current_connection()

        if conn is None:
            raise RuntimeError("No transaction active")

        await self._provider.commit_transaction(conn)
        self._set_current_connection(None)
        await self._provider.close_connection(conn)

    async def rollback_transaction(self):
        conn = self._get_current_connection()
        if conn is None:
            raise RuntimeError("No transaction active")

        await self._provider.rollback_transaction(conn)
        self._set_current_connection(None)
        await self._provider.close_connection(conn)

    def _get_current_connection(self) -> Any:
        return self._current_connection.get()

    def _set_current_connection(self, connection):
        return self._current_connection.set(connection)

    def _reset_current_connection(self, token):
        self._current_connection.reset(token)

    def debug(self, msg):  # pragma: no cover
        if self._debug is True:
            logger.debug(f" PG : {threading.current_thread().ident} {msg}")
