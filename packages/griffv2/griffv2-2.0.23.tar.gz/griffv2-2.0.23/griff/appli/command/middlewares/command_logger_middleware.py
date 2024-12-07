from loguru import logger

from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.message.message_middleware import MessageContext


class CommandLoggerMiddleware(CommandMiddleware):
    async def dispatch(
        self, message: Command, context: MessageContext | None = None
    ) -> CommandResponse:
        logger.info(f"dispatch command: {message.short_classname()}")
        logger.debug(message.model_dump())
        response = await self._next_dispatch(message, context)
        logger.debug(response.model_dump())
        return response
