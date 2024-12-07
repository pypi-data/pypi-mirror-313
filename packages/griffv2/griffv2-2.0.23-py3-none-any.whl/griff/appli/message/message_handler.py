from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar, Self, Any, Literal

from pydantic import BaseModel, model_validator

from griff.appli.message.message import Message
from griff.domain.common_types import EntityId
from griff.utils.errors import BaseError


class AbstractMessageResponse(BaseModel, ABC):
    code: int = 200
    content: Any | None = None
    is_success: bool

    @property
    def is_failure(self) -> bool:  # pragma: no cover
        return not self.is_success

    def dump_content(self) -> BaseModel | None:  # pragma: no cover
        if self.content:
            return self.content.model_dump()
        return self.content


class MessageSuccessResponse(AbstractMessageResponse):
    content: Any | None = None
    is_success: Literal[True] = True


class EntityIdContent(BaseModel):  # pragma: no cover
    entity_id: EntityId


class MessageErrorResponse(AbstractMessageResponse):
    code: int = 500
    content: BaseError
    is_success: Literal[False] = False

    @model_validator(mode="after")
    def set_code_from_error_code(self) -> Self:
        self.code = self.content.code
        return self


MessageResponse = MessageSuccessResponse | MessageErrorResponse | None
M = TypeVar("M", bound=Message)
MR = TypeVar("MR", bound=MessageResponse)


class MessageHandler(Generic[M, MR], ABC):
    @abstractmethod
    async def handle(self, message: M) -> MR:  # pragma: no cover
        pass

    @classmethod
    def handlers(cls):
        return cls.__subclasses__()

    @classmethod
    @abstractmethod
    def listen_to(cls) -> Type[M]:  # pragma: no cover
        pass
