from abc import ABC, abstractmethod
from typing import Type, List

from griff.context_entry_point import ContextEntryPoint
from griff.domain.common_types import Entity
from griff.infra.repository.repository import Repository
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase
from griff.utils.exceptions import EntityNotFoundException


class RepositoryTestCase(RuntimeTestMixin, TestCase, ABC):
    @classmethod
    @abstractmethod
    def entry_point_class(cls) -> Type[ContextEntryPoint]:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().repository_test(cls.entry_point_class())

    @staticmethod
    async def run_crud(
        repository: Repository,
        aggregates: List[Entity],
        aggregate_to_update: Entity,
        update_data: dict,
        aggregate_to_delete: Entity,
    ):
        # insert, read
        for aggregate in aggregates:
            await repository.save(aggregate)
        inserted_data = await repository.list_all()
        # update, read
        updated_aggregate = aggregate_to_update.model_copy(update=update_data)
        await repository.save(updated_aggregate)
        after_update = await repository.get_by_id(updated_aggregate.entity_id)
        # delete, read
        assert await repository.get_by_id(aggregate_to_delete.entity_id)
        await repository.delete(aggregate_to_delete)
        try:
            await repository.get_by_id(aggregate_to_delete.entity_id)
            assert False, "aggregate was not deleted"
        except EntityNotFoundException:
            assert True
        return {
            "inserted_data": inserted_data,
            "after_update": after_update,
        }
