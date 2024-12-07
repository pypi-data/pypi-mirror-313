from griff.appli.app_event.app_event import AppEvent
from griff.appli.event.event_dispatcher import EventDispatcher


class AppEventDispatcher(EventDispatcher[AppEvent, None]):
    ...
