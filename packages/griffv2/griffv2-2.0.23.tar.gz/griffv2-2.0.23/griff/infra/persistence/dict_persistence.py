import copy
from typing import Dict, List, Callable, Any

from griff.infra.persistence.persistence import (
    Persistence,
    QueryRowResult,
    QueryResult,
    QueryRowResults,
)
from griff.infra.persistence.serialized_persistence import SerializedPersistence
from griff.services.json.json_service import JsonService

QueryName = str
QueryCallable = Callable[..., QueryResult]


def _has_filters_match(data: Dict[str, Dict], filters: Dict[str, Any]) -> bool:
    for attr, value in filters.items():
        if data.get(attr) != value:
            return False
    return True


class DictPersistence(Persistence):
    def __init__(self, initial_data: List[Dict] | None = None):
        self._internal_storage: Dict[str, Dict] = {}
        self.reset(initial_data)

    async def _insert(self, data: dict) -> None:
        if data["entity_id"] not in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' already exists")

    async def _update(self, data: dict) -> None:
        if data["entity_id"] in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' does not exists")

    async def _delete(self, persistence_id: str) -> None:
        if persistence_id in self._internal_storage:
            self._internal_storage.pop(persistence_id)
            return None
        raise ValueError(f"id '{persistence_id}' does not exists")

    async def _get_by_id(self, persistence_id: str) -> QueryRowResult:
        if persistence_id in self._internal_storage:
            return copy.deepcopy(self._internal_storage[persistence_id])
        raise ValueError(f"id '{persistence_id}' not found")

    async def _list_all(self) -> QueryRowResults:
        return copy.deepcopy(list(self._internal_storage.values()))

    async def _run_query(self, query_name: str, **query_params) -> QueryResult:
        if self._has_custom_queries(query_name):
            return self._run_custom_queries(query_name, **query_params)
        if "list_all" == query_name:
            return copy.deepcopy(list(self._internal_storage.values()))
        if "get_by_" in query_name:
            return self._get_by_attrs(**query_params)
        if "list_by_" in query_name:
            return self._list_by_attrs(**query_params)
        raise RuntimeError(f"Query {query_name} not found")

    def reset(self, initial_data: List[Dict] | None = None):
        if initial_data is None:
            self._internal_storage = {}
            return None
        self._internal_storage = {
            e["entity_id"]: self._prepare_to_save(copy.deepcopy(e))
            for e in initial_data
        }

    @property
    def _queries(self) -> Dict[QueryName, QueryCallable]:
        return {}

    def _has_custom_queries(self, query_name: str) -> bool:
        return query_name in self._queries

    def _run_custom_queries(self, query_name: str, **query_params):
        return self._queries[query_name](**query_params)

    def _searchable_internal_storage(self):
        if self._internal_storage:
            return self._prepare_row_results(
                [copy.deepcopy(r) for r in self._internal_storage.values()]
            )
        return self._internal_storage  # pragma: no cover

    def _get_by_attrs(
        self, filtering_callable: Callable = _has_filters_match, **query_params
    ):
        for e in self._searchable_internal_storage():
            if filtering_callable(e, query_params):
                return self._internal_storage[e["entity_id"]]
        return None

    def _list_by_attrs(
        self, filtering_callable: Callable = _has_filters_match, **query_params
    ):
        result = []
        for e in self._searchable_internal_storage():
            if filtering_callable(e, query_params):
                result.append(self._internal_storage[e["entity_id"]])
        return result


class SerializedDictPersistence(SerializedPersistence, DictPersistence):
    def __init__(self, initial_data: List[Dict] | None = None):
        SerializedPersistence.__init__(self, JsonService())
        DictPersistence.__init__(self, initial_data)
