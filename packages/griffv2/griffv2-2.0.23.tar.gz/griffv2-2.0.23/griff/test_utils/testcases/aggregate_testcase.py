from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.uniqid_service import UniqIdService
from griff.test_utils.testcases.testcase import TestCase


class AggregateTestCase(TestCase):
    uniqid_service: UniqIdService

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.uniqid_service = UniqIdService(
            FakeUniqIdGenerator(999999999999999999999999999999990001)
        )

    def setup_method(self):
        super().setup_method()
        self.uniqid_service.reset()
