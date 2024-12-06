from abc import ABC, abstractmethod

from griff.services.hasher.hasher_models import UnHashedStr, HashedStr


class HasherProvider(ABC):
    @abstractmethod
    def hash(self, to_hash: UnHashedStr) -> HashedStr:  # pragma: no cover
        pass

    @abstractmethod
    def verify(
        self, candidate: UnHashedStr, reference: HashedStr
    ) -> bool:  # pragma: no cover
        pass
