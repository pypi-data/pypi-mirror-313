from injector import inject

from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.message.message_middleware import MessageContext
from griff.services.db.db_service import DbService


class CommandUowMiddleware(CommandMiddleware):
    @inject
    def __init__(self, db_service: DbService):
        super().__init__()
        self._db_service = db_service

    async def dispatch(
        self, message: Command, context: MessageContext | None = None
    ) -> CommandResponse:
        async with self._db_service.transaction():
            response = await self._next_dispatch(message, context)
        return response
