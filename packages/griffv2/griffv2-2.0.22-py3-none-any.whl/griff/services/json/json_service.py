import json
from _decimal import Decimal
from pathlib import Path
from typing import Any

import orjson
from injector import singleton
from pydantic import BaseModel

from griff.services.abstract_service import AbstractService
from griff.services.path.path_service import PathService


@singleton
class JsonService(AbstractService):
    _path_service = PathService()

    def to_json_dumpable(self, d):
        json_bytes = orjson.dumps(d, default=self._orjson_default)
        return orjson.loads(json_bytes)

    def dump(self, d):
        json_bytes = orjson.dumps(d, default=self._orjson_default)
        return json_bytes.decode("utf-8")

    @staticmethod
    def load_from_str(str_json: str):
        try:
            return json.loads(str_json)
        except json.decoder.JSONDecodeError as e:
            raise ValueError(f"Invalid json: {e}")

    def dump_to_file(self, data, filename, human_readable=False):
        default_args = {"obj": self.to_json_dumpable(data)}
        human_readable_args = {
            "indent": 4,
            "separators": (",", ": "),
            "default": str,
            # disable non-ASCII characters escape with \uXXXX sequences
            "ensure_ascii": False,
        }
        with open(filename, "w") as f:
            args = {**default_args, **{"fp": f}}
            if human_readable:
                args = {**args, **human_readable_args}
            json.dump(**args)

    def load_from_file(self, filename: str | Path) -> Any:
        self._path_service.check_exists(filename)
        with open(filename) as f:
            return json.load(f)

    @staticmethod
    def _orjson_default(data):
        if isinstance(data, Decimal):
            return str(data)

        if isinstance(data, bytes):
            return data.decode("utf-8")

        if isinstance(data, set):
            return list(data)

        if isinstance(data, BaseModel):
            return data.model_dump()

        raise TypeError
