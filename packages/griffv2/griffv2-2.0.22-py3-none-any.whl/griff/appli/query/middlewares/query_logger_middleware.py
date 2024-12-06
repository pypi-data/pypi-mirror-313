from loguru import logger

from griff.appli.message.message_middleware import MessageContext
from griff.appli.query.query import Query
from griff.appli.query.query_handler import QueryResponse
from griff.appli.query.query_middleware import QueryMiddleware


class QueryLoggerMiddleware(QueryMiddleware):
    async def dispatch(
        self, message: Query, context: MessageContext | None = None
    ) -> QueryResponse:
        logger.info(f"dispatch query: {message.short_classname()}")
        logger.debug(message.model_dump())
        response = await self._next_dispatch(message)
        logger.debug(response.model_dump())
        return response
