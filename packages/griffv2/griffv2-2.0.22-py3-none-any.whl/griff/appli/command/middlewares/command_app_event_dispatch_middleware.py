from injector import inject

from griff.appli.app_event.app_event import AppEvent
from griff.appli.app_event.app_event_bus import AppEventBus
from griff.appli.command.command import Command
from griff.appli.command.command_handler import CommandResponse
from griff.appli.command.command_middleware import CommandMiddleware
from griff.appli.message.message_middleware import MessageContext


class CommandAppEventDispatchMiddleware(CommandMiddleware):
    @inject
    def __init__(self, app_event_bus: AppEventBus):
        super().__init__()
        self._app_event_bus = app_event_bus

    async def dispatch(
        self, message: Command, context: MessageContext | None = None
    ) -> CommandResponse:
        response = await self._next_dispatch(message, context)
        if response.is_success:
            for event in response.events:
                if isinstance(event, AppEvent):
                    await self._app_event_bus.dispatch(event, context)
        return response
