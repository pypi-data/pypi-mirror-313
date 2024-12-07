from typing import Self, Generic

from griff.appli.event.event import Event
from griff.appli.message.message_dispatcher import MessageDispatcher, M, MR
from griff.appli.message.message_handler import MessageHandler
from griff.appli.message.message_middleware import MessageContext


class EventDispatcher(Generic[M, MR], MessageDispatcher[Event, None]):
    async def dispatch(
        self, message: Event, context: MessageContext | None = None
    ) -> None:
        if message.classname() not in self._handlers:
            return None

        for handler in self._handlers[message.classname()]:
            await handler.handle(message)

    def _register(self, handler: MessageHandler) -> Self:
        if handler.listen_to().classname() not in self._handlers:
            self._handlers[handler.listen_to().classname()] = []

        already_registered = any(
            handler.__class__ == h.__class__
            for h in self._handlers[handler.listen_to().classname()]
        )

        if already_registered:
            raise RuntimeError(
                f"Handler '{handler.__class__.__name__}' already registered"
            )

        self._handlers[handler.listen_to().classname()].append(handler)
        return self
