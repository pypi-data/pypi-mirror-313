from typing import Optional

from ulid import ULID

from griff.services.uniqid.generator.uniqid_generator import (
    UniqIdGenerator,
)


class UlidUniqIdGenerator(UniqIdGenerator):
    def next_id(self, name: Optional[str] = None) -> str:
        return str(ULID())

    def reset(self, start_id: int = 1) -> None:  # pragma: no cover
        pass
