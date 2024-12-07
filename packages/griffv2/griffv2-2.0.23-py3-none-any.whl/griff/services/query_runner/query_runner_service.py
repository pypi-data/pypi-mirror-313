from pathlib import Path
from typing import List

import aiosql
from injector import inject
from loguru import logger

from griff.services.abstract_service import AbstractService
from griff.services.db.db_service import DbService
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings


class QueryRunnerService(AbstractService):
    @inject
    def __init__(self, db_service: DbService, settings: QueryRunnerSettings):
        self._db_service = db_service
        self._sql_queries = None
        self._settings = settings

    async def run_query(self, query_name, **query_params):
        query = self.check_query_exists(query_name)
        async with self._db_service.connection() as conn:
            try:
                sql = query.sql.replace("\n", " ")
                logger.debug(f"'{query_name}':SQL: {sql}\nparams : {query_params}")
                results = await query(conn=conn, **query_params)
                return self._format_results(results)
            except Exception as exec_exception:
                raise RuntimeError(str(exec_exception))

    async def run_many_query(self, query_name, queries_params: List[dict]):
        query = self.check_query_exists(query_name)
        async with self._db_service.connection() as conn:
            try:
                results = await query(conn, queries_params)
                return self._format_results(results)
            except Exception as exec_exception:
                raise RuntimeError(str(exec_exception))

    def set_sql_queries(self, relative_sql_path: str) -> None:
        sql_path = Path(self._settings.project_dir).joinpath(relative_sql_path)
        self._sql_queries = aiosql.from_path(
            sql_path=str(sql_path), driver_adapter=self._settings.driver
        )

    def check_query_exists(self, query_name: str):
        try:
            return getattr(self._sql_queries, query_name)
        except AttributeError as e:
            raise RuntimeError(f"query '{query_name}' not found: {e}")

    @staticmethod
    def _format_results(results) -> dict | List[dict] | None:
        if results is None or isinstance(results, (str, int, float)):
            return None
        if isinstance(results, list):
            return [dict(row) for row in results]
        return dict(results)
