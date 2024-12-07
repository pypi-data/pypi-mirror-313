from typing import Optional

from injector import singleton

from griff.services.uniqid.generator.uniqid_generator import UniqIdGenerator


@singleton
class FakeUniqIdGenerator(UniqIdGenerator):
    def __init__(self, start_id=1):
        self._start = 0
        self._start = start_id - 1
        self._session = {"default": self._start}

    def next_id(self, name: Optional[str] = None) -> str:
        if name is None:
            name = "default"
        if name not in self._session:
            if len(name) >= 16:
                raise ValueError("Name is too long < 16")
            self._session[name] = self._start

        self._session[name] += 1
        return self._format_id(name)

    def reset(self, start_id: int = 1):
        self._start = start_id - 1
        self._session = {"default": self._start}

    def _format_id(self, name: str) -> str:
        if name == "default":
            return f"FAKEULID{self._session[name]:>018}"

        postfix = name.replace("_", "").upper()
        pad = 16 - len(postfix)
        return f"FAKEULID-{postfix}-{self._session[name]:>0{pad}}"
