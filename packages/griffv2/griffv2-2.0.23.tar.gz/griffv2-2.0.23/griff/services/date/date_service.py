import datetime
from typing import Optional

import arrow
from injector import singleton

from griff.services.abstract_service import AbstractService
from griff.services.date.date_models import DateTime


@singleton
class DateService(AbstractService):
    def __init__(self, locale="fr-fr"):
        self._locale = locale

    def now(self) -> DateTime:
        return DateTime(arrow.utcnow())

    def to_mysql_date(self, d: DateTime | None = None) -> str:
        return self._get(d).to_mysql_date()

    def to_mysql_datetime(self, d: DateTime | None = None) -> str:
        return self._get(d).to_mysql_datetime()

    def to_date(self, d: DateTime | None = None) -> datetime.date:
        return self._get(d).to_date()

    def to_datetime(self, d: DateTime | None = None) -> datetime.datetime:
        return self._get(d).to_datetime()

    def _get(self, d: Optional[DateTime] = None):
        if d and isinstance(d, DateTime) is False:
            raise ValueError("Invalid DateTime or Date instance")
        return self.now() if d is None else d
