import copy
from abc import ABC
from typing import Self

from injector import inject

from griff.infra.persistence.persistence import Persistence, QueryRowResult
from griff.services.json.json_service import JsonService


class SerializedPersistence(Persistence, ABC):
    @inject
    def __init__(self, json_service: JsonService):
        self.json_service = json_service
        self._metadata_fields = ["created_at", "updated_at"]
        self._set_excluded_fields(
            [*self._metadata_fields, *self._serialize_excluded_fields]
        )

    def add_excluded_field(self, field: str) -> Self:
        # à utiliser uniquement dans un repository
        if field not in self._excluded_fields:
            self._excluded_fields.append(field)
        return self

    @property
    def _serialized_persistence_fieldname(self):
        return "serialized"

    @property
    def _serialize_excluded_fields(self):
        return []

    def _set_excluded_fields(self, fields: list[str]) -> None:
        self._excluded_fields = list(dict.fromkeys(fields))

    def _prepare_to_save(self, data: dict) -> dict:
        data_to_serialize = {
            k: v for k, v in data.items() if not self._is_field_serialize_excluded(k)
        }
        attr_serialized = data_to_serialize.keys()
        json_prepared = self.json_service.to_json_dumpable(data_to_serialize)
        return {
            "entity_id": data["entity_id"],
            self._serialized_persistence_fieldname: self.json_service.dump(
                json_prepared
            ),
            **{k: v for k, v in data.items() if k not in attr_serialized},
        }

    def _prepare_row_result(self, result: QueryRowResult) -> QueryRowResult:
        result_copy = copy.deepcopy(result)
        serialized = result_copy.pop(self._serialized_persistence_fieldname)
        return {**result_copy, **self.json_service.load_from_str(serialized)}

    def _is_field_serialize_excluded(self, field_name) -> bool:
        return field_name in self._excluded_fields
