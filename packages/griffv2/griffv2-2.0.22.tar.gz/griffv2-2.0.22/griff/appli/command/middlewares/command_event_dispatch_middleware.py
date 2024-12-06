from injector import inject

from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.event.event_bus import EventBus
from griff.appli.message.message_middleware import MessageContext


class CommandEventDispatchMiddleware(CommandMiddleware):
    @inject
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self._event_bus = event_bus

    async def dispatch(
        self, message: Command, context: MessageContext | None = None
    ) -> CommandResponse:
        response = await self._next_dispatch(message, context)
        if response.is_success:
            for event in response.events:
                await self._event_bus.dispatch(event, context)
        return response
