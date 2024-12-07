from griff.test_utils.testcases.domain_testcase import DomainTestCase
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_domain import {{ cookiecutter.command | snake_case }}, Action{{cookiecutter.aggregate | pascal_case}}

class Test{{ cookiecutter.command | pascal_case }}Domain(DomainTestCase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.dtf = {{ cookiecutter.context | pascal_case }}Dtf(start_id=99990)
        {{ cookiecutter.aggregate | snake_case }} = cls.dtf.creer_{{ cookiecutter.aggregate | snake_case }}()
        cls.{{ cookiecutter.aggregate | snake_case }}_action = Action{{cookiecutter.aggregate | pascal_case}}(**{{ cookiecutter.aggregate | snake_case }}.model_dump())

    def setup_method(self):
        super().setup_method()

    """
    {{ cookiecutter.command | snake_case }}
    """

    def test_{{ cookiecutter.command | snake_case }}_reussi(self):
        actual = {{ cookiecutter.command | snake_case }}(self.{{ cookiecutter.aggregate | snake_case }}_action)
        self.assert_equals_resultset(actual.model_dump())
