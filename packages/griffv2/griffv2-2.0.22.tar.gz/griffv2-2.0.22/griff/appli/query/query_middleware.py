from abc import ABC, abstractmethod

from griff.appli.message.message_middleware import MessageMiddleware, MessageContext
from griff.appli.query.query import Query
from griff.appli.query.query_handler import QueryResponse


class QueryMiddleware(MessageMiddleware[Query, QueryResponse], ABC):
    @abstractmethod
    async def dispatch(
        self, message: Query, context: MessageContext | None = None
    ) -> QueryResponse:
        pass
