from loguru import logger

from griff.appli.event.event import Event
from griff.appli.event.event_middleware import EventMiddleware
from griff.appli.message.message_middleware import MessageContext


class EventLoggerMiddleware(EventMiddleware):
    async def dispatch(
        self, message: Event, context: MessageContext | None = None
    ) -> None:
        logger.info(f"dispatch event: {message.short_classname()}")
        logger.debug(message.model_dump())
        await self._next_dispatch(message, context)
