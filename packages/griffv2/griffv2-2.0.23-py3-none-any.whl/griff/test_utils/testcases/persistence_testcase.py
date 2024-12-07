import copy
from abc import ABC, abstractmethod
from typing import Type, List

from griff.context_entry_point import ContextEntryPoint
from griff.infra.persistence.persistence import Persistence
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase


class PersistenceTestCase(RuntimeTestMixin, TestCase, ABC):
    @classmethod
    @abstractmethod
    def entry_point_class(cls) -> Type[ContextEntryPoint]:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().persistence_test(cls.entry_point_class())

    def setup_method(self):
        super().setup_method()

    async def run_crud(
        self,
        persistence: Persistence,
        rows: List[dict],
        row_to_update: dict,
        update_data: dict,
        row_to_delete: dict,
    ):
        # insert, read
        for row in rows:
            await persistence.insert(row)
        inserted_data = await persistence.list_all()
        # update, read
        before_update = row_to_update
        updated_row = {**copy.deepcopy(before_update), **update_data}
        await persistence.update(updated_row)
        after_update = await persistence.get_by_id(before_update["entity_id"])
        # delete, read
        await persistence.delete(row_to_delete["entity_id"])
        assert await persistence.get_by_id(row_to_delete["entity_id"]) is None
        return {
            "inserted_data": inserted_data,  # type: ignore
            "after_update": after_update,
        }
