import abc
from typing import Optional


class UniqIdGenerator(abc.ABC):
    @abc.abstractmethod
    def next_id(self, name: Optional[str] = None) -> str:
        ...  # pragma: no cover

    @abc.abstractmethod
    def reset(self, start_id: int = 1) -> None:  # pragma: no cover
        pass
