from typing import TypeAlias, Type

from griff.appli.policies.policy import PolicyException
from griff.appli.command.command import Command
from griff.appli.command.command_handler import (
    CommandHandler,
    CommandErrorResponse,
    CommandSuccessResponse,
)
from injector import inject
from shared_kernel.domain.permission import PermissionAdminRequired
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_domain import {{ cookiecutter.command | snake_case }}, Action{{cookiecutter.aggregate | pascal_case}}
from {{ cookiecutter.context | snake_case }}._common.domain.{{ cookiecutter.aggregate | snake_case }} import Base{{cookiecutter.aggregate | pascal_case}}, {{cookiecutter.aggregate | pascal_case}}
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import {{cookiecutter.aggregate | pascal_case}}Repository
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_event import {{ cookiecutter.CommandEvent }}

from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_policies import {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucPolicy, {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucError


class {{ cookiecutter.command | pascal_case }}Command(Base{{cookiecutter.aggregate | pascal_case}}, PermissionAdminRequired, Command):
    ...

class {{ cookiecutter.command | pascal_case }}SuccessResponse(CommandSuccessResponse):
    content: {{cookiecutter.aggregate | pascal_case}}


{{ cookiecutter.command | pascal_case }}Error = {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucError


class {{ cookiecutter.command | pascal_case }}ErrorResponse(CommandErrorResponse):
    content: {{ cookiecutter.command | pascal_case }}Error


{{ cookiecutter.command | pascal_case }}Response: TypeAlias = (
    {{ cookiecutter.command | pascal_case }}SuccessResponse | {{ cookiecutter.command | pascal_case }}ErrorResponse
)


class {{ cookiecutter.command | pascal_case }}Handler(
    CommandHandler[{{ cookiecutter.command | pascal_case }}Command, {{ cookiecutter.command | pascal_case }}Response]
):
    @inject
    def __init__(
        self, {{ cookiecutter.aggregate | snake_case }}_repository: {{cookiecutter.aggregate | pascal_case}}Repository, {{ cookiecutter.aggregate | snake_case }}_verifie_un_truc_policy: {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucPolicy
    ):
        super().__init__()
        self.repository = {{ cookiecutter.aggregate | snake_case }}_repository
        self.{{ cookiecutter.aggregate | snake_case }}_verifie_un_truc_policy = {{ cookiecutter.aggregate | snake_case }}_verifie_un_truc_policy

    async def handle(self, command: {{ cookiecutter.command | pascal_case }}Command) -> {{ cookiecutter.command | pascal_case }}Response:
        try:
            await self.{{ cookiecutter.aggregate | snake_case }}_verifie_un_truc_policy.check()
        except PolicyException as policy_exception:
            return {{ cookiecutter.command | pascal_case }}ErrorResponse(content=policy_exception.error)

        {{ cookiecutter.aggregate | snake_case }} = {{ cookiecutter.command | snake_case }}(Action{{cookiecutter.aggregate | pascal_case}}(**command.model_dump()))
        await self.repository.save({{ cookiecutter.aggregate | snake_case }})
        event = {{ cookiecutter.CommandEvent }}(payload={{ cookiecutter.aggregate | snake_case }})
        return {{ cookiecutter.command | pascal_case }}SuccessResponse(content={{ cookiecutter.aggregate | snake_case }}, events=[event])

    @classmethod
    def listen_to(cls) -> Type[{{ cookiecutter.command | pascal_case }}Command]:
        return {{ cookiecutter.command | pascal_case }}Command
