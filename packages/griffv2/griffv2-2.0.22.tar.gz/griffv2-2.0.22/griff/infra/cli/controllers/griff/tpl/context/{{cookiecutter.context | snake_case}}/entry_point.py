from griff.context_entry_point import ContextEntryPoint
from injector import inject

from {{ cookiecutter.context | snake_case }}._common.{{ cookiecutter.context | snake_case }}_cli_router import {{ cookiecutter.context | pascal_case }}CliRouter
from {{ cookiecutter.context | snake_case }}._common.{{ cookiecutter.context | snake_case }}_router import {{ cookiecutter.context | pascal_case }}ApiRouter

class {{ cookiecutter.context | pascal_case }}EntryPoint(ContextEntryPoint[{{ cookiecutter.context | pascal_case }}ApiRouter, {{ cookiecutter.context | pascal_case }}CliRouter]):
    @inject
    def __init__(self, api_router: {{ cookiecutter.context | pascal_case }}ApiRouter, cli_router: {{ cookiecutter.context | pascal_case }}CliRouter):
        super().__init__(api_router, cli_router)

    @staticmethod
    def context_name() -> str:
        return "{{ cookiecutter.context | snake_case }}"
