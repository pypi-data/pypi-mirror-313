from injector import singleton, inject

from griff.services.abstract_service import AbstractService
from griff.services.hasher.hasher_models import UnHashedStr, HashedStr
from griff.services.hasher.providers.hasher_provider import HasherProvider


@singleton
class HasherService(AbstractService):
    @inject
    def __init__(self, hasher_provider: HasherProvider):
        self._hasher_provider = hasher_provider

    def hash(self, to_hash: UnHashedStr) -> HashedStr:
        return self._hasher_provider.hash(to_hash)

    def verify(self, candidate: UnHashedStr, reference: HashedStr) -> bool:
        return self._hasher_provider.verify(candidate, reference)
