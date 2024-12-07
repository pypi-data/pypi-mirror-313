from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.message.message_dispatcher import MessageDispatcher


class CommandDispatcher(MessageDispatcher[Command, CommandResponse]):
    ...
