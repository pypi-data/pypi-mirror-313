from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from injector import singleton

from griff.services.hasher.providers.hasher_provider import (
    HasherProvider,
    UnHashedStr,
    HashedStr,
)


@singleton
class Argon2Provider(HasherProvider):
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, to_hash: UnHashedStr) -> HashedStr:
        return self.ph.hash(to_hash)

    def verify(self, candidate: UnHashedStr, reference: HashedStr) -> bool:
        try:
            return self.ph.verify(reference, candidate)
        except (VerificationError, InvalidHashError):
            return False
