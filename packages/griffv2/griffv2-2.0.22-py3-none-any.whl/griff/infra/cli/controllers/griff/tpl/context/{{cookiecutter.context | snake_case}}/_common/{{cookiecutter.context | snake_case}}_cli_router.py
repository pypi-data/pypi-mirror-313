from griff.infra.cli.cli_router import CliRouter
from injector import inject, singleton


@singleton
class {{ cookiecutter.context | pascal_case }}CliRouter(CliRouter):
    @inject
    def __init__(self):
        super().__init__()
        # self._app.add_typer(ctrl.get_app(), name=ctrl.get_command_name())

    def get_command_group_name(self) -> str:  # pragma: no cover
        return "{{ cookiecutter.context | snake_case }}"
