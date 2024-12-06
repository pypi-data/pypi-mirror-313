from injector import inject, singleton

from griff.services.db.db_service import DbService
from griff.services.db.providers.db_provider import DbProvider


@singleton
class DbTestService(DbService):
    @inject
    def __init__(self, provider: DbProvider):
        super().__init__(provider)
        self._current_connection = None  # type: ignore

    def _get_current_connection(self):
        return self._current_connection

    def _set_current_connection(self, connection):
        self._current_connection = connection
        return None

    def _reset_current_connection(self, token):  # pragma: no cover
        self._current_connection = None
