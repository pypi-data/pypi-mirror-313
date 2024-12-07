from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer
from griff.appli.command.command_bus import CommandBus
from griff.infra.api.api_controller import ApiController
from griff.infra.api.register_endpoint import register_endpoint
from injector import inject

from {{ cookiecutter.context | snake_case }}._common.api.{{ cookiecutter.context | snake_case }}_schemas import {{ cookiecutter.command | pascal_case }}In, {{ cookiecutter.command | pascal_case }}Out
from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_command import {{ cookiecutter.command | pascal_case }}Command

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/{{ cookiecutter.context | snake_case }}/{{ cookiecutter.command | snake_case }}")


class {{ cookiecutter.command | pascal_case }}Controller(ApiController):
    base_route = "/"

    @inject
    def __init__(self, command_bus: CommandBus):
        super().__init__()
        self._command_bus = command_bus

    @register_endpoint(
        route="/{{ cookiecutter.command | snake_case }}", method="POST", success_code=status.HTTP_200_OK
    )
    async def {{ cookiecutter.command | snake_case }}(self, payload: {{ cookiecutter.command | pascal_case }}In, token: str = Depends(oauth2_scheme)) -> {{ cookiecutter.command | pascal_case }}Out:
        command = {{ cookiecutter.command | pascal_case }}Command(**payload.model_dump())
        response = await self._command_bus.dispatch(command, context=self._get_token_context(token))
        return self.prepare_response(response)
