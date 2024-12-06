from abc import ABC
from typing import Dict, Generic, Self, TypeVar

from griff.appli.message.message_handler import (
    Message,
    MessageHandler,
    MessageResponse,
)
from griff.appli.message.message_middleware import MessageMiddleware, MessageContext

M = TypeVar("M", bound=Message)
MR = TypeVar("MR", bound=MessageResponse | None)
MH = TypeVar("MH", bound=MessageHandler)
HandlerList = Dict[str, MH]


class MessageDispatcher(Generic[M, MR], MessageMiddleware[M, MR], ABC):
    def __init__(self) -> None:
        super().__init__()
        self._handlers: HandlerList = {}

    async def dispatch(self, message: M, context: MessageContext | None = None) -> MR:
        if message.classname() not in self._handlers:
            raise RuntimeError(
                f"No handler registered for '{message.short_classname()}'"
            )
        response = await self._handlers[message.classname()].handle(message)
        return response

    def set_next(self, middleware: MessageMiddleware) -> MessageMiddleware:
        raise RuntimeError(f"{self.__class__.__name__} must be the last middleware")

    def register(self, handlers: list[MH]) -> Self:
        for handler in handlers:
            self._register(handler)
        return self

    def _register(self, handler: MessageHandler) -> Self:
        if handler.listen_to().classname() in self._handlers:
            raise RuntimeError(
                f"Handler '{handler.__class__.__name__}' already registered"
            )
        # noinspection PyTypeChecker
        self._handlers[handler.listen_to().classname()] = handler
        return self
