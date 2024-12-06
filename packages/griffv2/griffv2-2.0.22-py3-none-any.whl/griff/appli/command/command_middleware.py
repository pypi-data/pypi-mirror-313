from abc import ABC, abstractmethod

from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.message.message_middleware import MessageMiddleware, MessageContext


class CommandMiddleware(MessageMiddleware[Command, CommandResponse], ABC):
    @abstractmethod
    async def dispatch(
        self, message: Command, context: MessageContext | None = None
    ) -> CommandResponse:
        pass
