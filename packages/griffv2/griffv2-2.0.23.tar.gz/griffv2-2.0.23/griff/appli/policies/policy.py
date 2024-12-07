from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from griff.utils.errors import BaseError

E = TypeVar("E", bound=BaseError)


class PolicyException(Generic[E], Exception):
    def __init__(self, error: E) -> None:
        self.error = error


class Policy(ABC):
    @abstractmethod
    async def check(self, **kwargs) -> None:
        ...
