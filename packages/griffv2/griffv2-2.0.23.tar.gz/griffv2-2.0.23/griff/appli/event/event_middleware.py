from abc import ABC, abstractmethod

from griff.appli.event.event import Event
from griff.appli.message.message_middleware import MessageMiddleware, MessageContext


class EventMiddleware(MessageMiddleware[Event, None], ABC):
    @abstractmethod
    async def dispatch(
        self, message: Event, context: MessageContext | None = None
    ) -> None:
        pass
