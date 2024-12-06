from typing import Optional

import injector

from griff.services.abstract_service import AbstractService
from griff.services.uniqid.generator.uniqid_generator import (
    UniqIdGenerator,
)


class UniqIdService(AbstractService):
    @injector.inject
    def __init__(self, generator: UniqIdGenerator):
        self._generator = generator

    def get(self, name: Optional[str] = None) -> str:
        return self._generator.next_id(name)

    def reset(self, start_id=1):
        self._generator.reset(start_id)
