from abc import ABC
from typing import TypeVar, Generic, List, Any, Literal

from pydantic import Field
from pydantic.main import IncEx

from griff.appli.command.command import Command
from griff.appli.event.event import Event
from griff.appli.message.message_handler import (
    MessageHandler,
    MessageErrorResponse,
    MessageSuccessResponse,
    EntityIdContent,
)
from griff.infra.registry.meta_registry import MetaCommandHandlerRegistry


class CommandSuccessResponse(MessageSuccessResponse, ABC):
    events: List[Event] = Field(default_factory=list)

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        serialize_as_any: bool = False
    ) -> dict[str, Any]:
        result = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        # pydantic dump model as only Event ignoring specific event fields
        result["events"] = [e.model_dump() for e in self.events]
        return result


class CommandErrorResponse(MessageErrorResponse, ABC):
    ...


class CommandEntityIdResponse(CommandSuccessResponse):  # pragma: no cover
    content: EntityIdContent


CommandResponse = CommandSuccessResponse | CommandErrorResponse

CM = TypeVar("CM", bound=Command)
CR = TypeVar("CR", bound=CommandResponse)


class CommandHandler(
    Generic[CM, CR], MessageHandler[CM, CR], ABC, metaclass=MetaCommandHandlerRegistry
):
    ...
