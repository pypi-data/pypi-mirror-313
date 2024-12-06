from abc import ABC
from typing import TypeVar, Generic

from griff.appli.app_event.app_event import AppEvent
from griff.appli.message.message_handler import (
    MessageHandler,
)
from griff.infra.registry.meta_registry import (
    MetaAppEventHandlerRegistry,
)

EM = TypeVar("EM", bound=AppEvent)


class AppEventHandler(
    Generic[EM], MessageHandler[EM, None], ABC, metaclass=MetaAppEventHandlerRegistry
):
    ...
