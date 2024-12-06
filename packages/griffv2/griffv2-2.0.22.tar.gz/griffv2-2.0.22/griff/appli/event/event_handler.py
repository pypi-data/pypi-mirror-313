from abc import ABC
from typing import TypeVar, Generic, Type, Any

from griff.appli.event.event import Event
from griff.appli.message.message_handler import (
    MessageHandler,
)
from griff.infra.registry.meta_registry import (
    MetaEventHandlerRegistry,
)

EM = TypeVar("EM", bound=Event)


class EventHandler(
    Generic[EM], MessageHandler[EM, None], ABC, metaclass=MetaEventHandlerRegistry
):
    ...


class FakeEventHandler(EventHandler, ABC):
    on_event_type: Type[Event]

    def __init__(self):
        super().__init__()
        self._log = {}

    async def handle(self, message: Event) -> None:
        self._log[message.event_name] = message.model_dump()  # type: ignore

    def list_events_handled(self) -> dict[str, Any]:
        return self._log

    @classmethod
    def listen_to(cls) -> Type[Event]:
        return cls.on_event_type
