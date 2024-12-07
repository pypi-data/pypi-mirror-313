from pathlib import Path

from cookiecutter.main import cookiecutter

from griff.infra.cli.cli_controller import CliController
from griff.infra.cli.register_cli_command import register_cli_command


class GriffCliController(CliController):
    def __init__(self):
        super().__init__()
        self.root_tpl_path = Path(__file__).parent.joinpath("tpl")

    def get_command_name(self) -> str:
        return "griff"

    @register_cli_command(name="start-context")
    def start_context(self, context_name: str, output_dir=".", no_input=False):
        tpl_path = self.root_tpl_path.joinpath("context")
        cookiecutter(
            str(tpl_path),
            output_dir=output_dir,
            overwrite_if_exists=True,
            skip_if_file_exists=True,
            no_input=no_input,
            extra_context={"context": context_name},
        )
        return None

    @register_cli_command(name="start-agg")
    def start_agg(
        self,
        context_name: str,
        aggregate_name: str,
        output_dir=".",
        no_input=False,
    ):
        tpl_path = self.root_tpl_path.joinpath("aggregate")
        cookiecutter(
            str(tpl_path),
            output_dir=output_dir,
            no_input=no_input,
            overwrite_if_exists=True,
            skip_if_file_exists=True,
            extra_context={
                "context": context_name,
                "aggregate": aggregate_name,
            },
        )
        return None

    @register_cli_command(name="start-command")
    def start_command(
        self,
        context_name: str,
        aggregate_name: str,
        command_name: str,
        output_dir=".",
        no_input=False,
    ):
        tpl_path = self.root_tpl_path.joinpath("command")
        cookiecutter(
            str(tpl_path),
            output_dir=output_dir,
            no_input=no_input,
            overwrite_if_exists=True,
            skip_if_file_exists=True,
            extra_context={
                "context": context_name,
                "aggregate": aggregate_name,
                "command": command_name,
            },
        )
        return None
