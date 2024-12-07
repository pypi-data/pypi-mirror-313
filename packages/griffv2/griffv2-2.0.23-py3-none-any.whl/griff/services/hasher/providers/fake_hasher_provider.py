from griff.services.hasher.providers.hasher_provider import (
    HasherProvider,
    UnHashedStr,
    HashedStr,
)


class FakeHasherProvider(HasherProvider):
    def hash(self, to_hash: UnHashedStr) -> HashedStr:
        return to_hash.replace(" ", "µ")

    def verify(self, candidate: UnHashedStr, reference: HashedStr) -> bool:
        return candidate.replace(" ", "µ") == reference
