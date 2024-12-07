import hashlib
import json
from typing import Any

from griff.services.json.json_service import JsonService


class StubMixin:
    def __init__(self):
        self._calls = {}
        self._stub = {}
        self._stub_with_arguments = {}

    def reset_stub(self):
        self._calls = {}
        self._stub = {}

    def list_calls(self):
        return self._calls

    def call_count(self, method) -> int:
        return len([c for c in self._calls if method in c])

    def stub(
        self, method, response: Any | None = None, responses: list | None = None
    ):  # pragma: no cover
        if responses is None:
            self._stub[method] = [response]
            return None
        self._stub[method] = responses

    def _hash_payload(self, payload: dict):
        dhash = hashlib.md5()
        encoded = json.dumps(
            JsonService().to_json_dumpable(payload), sort_keys=True
        ).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    def stub_with_argument(self, method, arguments: dict, response):  # pragma: no cover
        _hashed_arguments = self._hash_payload(arguments)
        if method not in self._stub_with_arguments:
            self._stub_with_arguments[method] = {}
        self._stub_with_arguments[method][_hashed_arguments] = response

    def _call_stub(self, default_response=None) -> Any:
        name, payload = self._get_caller()

        self._register_call(name, payload)
        if name in self._stub:
            return self._render_stub(name)

        _hashed_arguments = self._hash_payload(payload)
        if (
            name in self._stub_with_arguments
            and _hashed_arguments in self._stub_with_arguments[name]
        ):
            return self._render_stub_with_argument(name, _hashed_arguments)

        return default_response

    def _register_call(self, method, payload):
        if method not in self._calls:
            self._calls[method] = []
        self._calls[method].append(payload)

    @staticmethod
    def _get_caller():
        import inspect

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        method_name = calframe[2][3]
        payload = calframe[2].frame.f_locals
        if "self" in payload:
            payload.pop("self")
        return method_name, payload

    def _render_stub_with_argument(self, method, hashed_arguments):  # pragma: no cover
        response = self._stub_with_arguments[method].pop(hashed_arguments)
        if isinstance(response, Exception):
            raise response
        return response

    def _render_stub(self, method):  # pragma: no cover
        response = self._stub[method].pop(0)
        if not self._stub[method]:
            self._stub.pop(method)
        if isinstance(response, Exception):
            raise response
        return response
