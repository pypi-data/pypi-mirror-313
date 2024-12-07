import datetime
from abc import ABC
from typing import Any

from pydantic import computed_field, Field

from griff.appli.message.message import Message
from griff.services.date.date_service import DateService
from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.uniqid_service import UniqIdService


class Event(Message, ABC):
    id: str = Field(
        default_factory=lambda: ServiceLocator.get(UniqIdService).get("event")
    )
    payload: Any
    created_at: datetime.datetime = Field(
        default_factory=lambda: ServiceLocator.get(DateService).to_datetime()
    )

    @computed_field
    def event_name(self) -> str:  # pragma: no cover
        return self.short_classname()
