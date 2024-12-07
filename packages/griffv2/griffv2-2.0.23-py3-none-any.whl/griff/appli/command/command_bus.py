from injector import inject

from griff.appli.command.command import Command
from griff.appli.command.command_dispatcher import CommandDispatcher
from griff.appli.command.command_handler import CommandResponse, CommandHandler
from griff.appli.message.message_bus import MessageBus


class CommandBus(MessageBus[Command, CommandResponse, CommandHandler]):
    @inject
    def __init__(self, dispatcher: CommandDispatcher) -> None:
        super().__init__(dispatcher)
