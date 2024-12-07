from griff.services.date.date_models import DateTime
from griff.services.date.date_service import DateService


class FakeDateService(DateService):
    def __init__(self):
        super().__init__()
        self._today = "2023-04-08 11:11:11.111111"

    def set_today(self, today: str):  # pragma: no cover
        self._today = today

    def now(self) -> DateTime:
        return DateTime(self._today)
