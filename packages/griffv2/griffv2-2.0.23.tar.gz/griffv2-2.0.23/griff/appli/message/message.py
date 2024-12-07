from abc import ABC

from pydantic import BaseModel, ConfigDict


class Message(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def classname(cls) -> str:
        return str(cls)

    @classmethod
    def short_classname(cls) -> str:
        return cls.__name__
