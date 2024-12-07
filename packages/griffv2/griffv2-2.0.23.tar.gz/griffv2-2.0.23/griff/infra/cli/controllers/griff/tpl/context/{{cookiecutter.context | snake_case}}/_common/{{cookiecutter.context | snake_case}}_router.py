from typing import List, Any

from griff.infra.api.api_router import ApiRouter
from injector import inject


{{ cookiecutter.context | pascal_case }}Controller = Any


class {{ cookiecutter.context | pascal_case }}ApiRouter(ApiRouter):
    @inject
    def __init__(self) -> None:
        self.ctrls: List[{{ cookiecutter.context | pascal_case }}Controller] = []
        super().__init__()

    def _list_controllers(self) -> List[{{ cookiecutter.context | pascal_case }}Controller]:
        return self.ctrls

    @property
    def _route_prefix(self) -> str:
        return "/{{ cookiecutter.context | snake_case }}"

    @property
    def _route_tags(self) -> List[str]:
        return ["{{ cookiecutter.context | snake_case }}"]
