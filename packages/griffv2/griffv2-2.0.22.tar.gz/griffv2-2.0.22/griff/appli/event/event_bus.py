from injector import inject

from griff.appli.event.event import Event
from griff.appli.event.event_dispatcher import EventDispatcher
from griff.appli.event.event_handler import EventHandler
from griff.appli.message.message_bus import MessageBus


class EventBus(MessageBus[Event, None, EventHandler]):
    @inject
    def __init__(self, dispatcher: EventDispatcher) -> None:
        super().__init__(dispatcher)
