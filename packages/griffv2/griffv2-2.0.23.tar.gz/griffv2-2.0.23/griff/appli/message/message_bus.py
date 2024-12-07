from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from griff.appli.message.message import Message
from griff.appli.message.message_dispatcher import MessageDispatcher
from griff.appli.message.message_handler import MessageResponse, MessageHandler
from griff.appli.message.message_middleware import MessageMiddleware, MessageContext

M = TypeVar("M", bound=Message)
MR = TypeVar("MR", bound=MessageResponse)
MH = TypeVar("MH", bound=MessageHandler)
ListMiddlewares = List[MessageMiddleware]


class MessageBus(Generic[M, MR, MH], ABC):
    @abstractmethod
    def __init__(self, dispatcher: MessageDispatcher) -> None:
        self._dispatcher = dispatcher
        self._middleware: MessageMiddleware | None = None

    def initialize(self, handlers: List[MH], middlewares: ListMiddlewares) -> None:
        self._register_handlers(handlers)
        self._register_middlewares(middlewares)

    async def dispatch(self, message: M, context: MessageContext | None = None) -> MR:
        if self.is_initialized() is False:
            raise RuntimeError(f"{self.__class__.__name__} not initialized")
        return await self._middleware.dispatch(message, context)  # type: ignore

    def is_initialized(self) -> bool:
        return self._middleware is not None

    def _register_middlewares(self, middlewares: ListMiddlewares) -> None:
        # dispatcher must be the last one
        all_middlewares = middlewares + [self._dispatcher]
        middleware = all_middlewares[0]
        for next_middleware in all_middlewares[1:]:
            middleware.set_next(next_middleware)
            middleware = next_middleware
        self._middleware = all_middlewares[0]

    def _register_handlers(self, handlers: List[MH]) -> None:
        self._dispatcher.register(handlers)
