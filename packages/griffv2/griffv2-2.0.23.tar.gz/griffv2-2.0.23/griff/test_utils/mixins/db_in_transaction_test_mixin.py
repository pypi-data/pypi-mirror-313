from abc import ABC

from griff.test_utils.mixins.db_test_mixin import DbTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory


class DbInTransactionTestMixin(DbTestMixin, ABC):
    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().test_with_db().with_test_in_db_transaction()
