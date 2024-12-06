import subprocess
from pathlib import Path

import typer
from injector import inject

from griff.infra.cli.cli_controller import (
    CliController,
)
from griff.infra.cli.register_cli_command import register_cli_command
from griff.infra.cli.typer_print import TyperPrint
from griff.services.path.path_service import PathService
from griff.settings.griff_settings import GriffSettings


class I18nCliController(CliController):
    @inject
    def __init__(self, settings: GriffSettings):
        super().__init__()
        self._settings = settings
        if settings.locale is None:
            raise ValueError("Locale settings are not defined")
        self._locale_settings = settings.locale

    def get_command_name(self):
        return "i18n"

    @register_cli_command(name="create")
    def init(self):
        TyperPrint.info(f"Initialize locale in {self._locale_settings.relative_path}")
        path_service = PathService()
        path_service.create_missing(self._settings.full_locale_path)
        path_service.create_missing(self._settings.pydantic_locale_path)
        path_service.create_missing(self._locale_settings.fastapi_locale_dir_name)
        p = self._extract_messages()
        self._check_process_run(p, "initialization")
        TyperPrint.success("Locale has been initialized")

    @register_cli_command(name="add_lang")
    def add_lang(self, lang: str):
        TyperPrint.info(f"Adding lang '{lang}'")
        self._check_pydantic_lang_exists(lang)
        pot_filename = self._check_pot_filename_exists()
        p = subprocess.run(
            f"pybabel init -l {lang} -i {pot_filename} -d "
            f"{self._locale_settings.relative_path}",
            shell=True,
        )
        self._check_process_run(p, "adding lang")
        TyperPrint.success(f"Lang '{lang}' has been added")

    @register_cli_command(name="compilemessages")
    def compile(self):
        TyperPrint.info("Translations compiling")
        p = subprocess.run(
            f"pybabel compile -d {self._settings.fastapi_local_path}", shell=True
        )
        self._check_process_run(p, "compilation")
        p = subprocess.run(
            f"pybabel compile -d {self._settings.pydantic_locale_path}",
            shell=True,
        )
        self._check_process_run(p, "compilation pydantic")
        TyperPrint.success("Translation messages have been compiled")

    @register_cli_command(name="update")
    def update(self):
        TyperPrint.info("Translations updating")
        self._extract_messages()
        pot_filename = self._check_pot_filename_exists()
        p = subprocess.run(
            f"pybabel update -i {pot_filename} -d "
            f"{self._locale_settings.relative_path}",
            shell=True,
        )
        self._check_process_run(p, "updating")
        TyperPrint.success("Translation messages have been updated")

    def _extract_messages(self):
        babel_config = f"{self._settings.project_dir}/babel.cfg"
        p = subprocess.run(
            f"pybabel extract . -F {babel_config} -o {self._get_messages_filename()}",
            shell=True,
        )
        return p

    def _get_messages_filename(self) -> Path:
        return Path(self._settings.project_dir).joinpath(
            self._locale_settings.relative_path, "messages.pot"
        )

    def _check_pydantic_lang_exists(self, lang):
        pydantic_lang_path = Path(self._settings.project_dir).joinpath(
            self._settings.pydantic_locale_path, lang.lower()
        )
        if pydantic_lang_path.exists() is False:
            TyperPrint.error(
                f"Pydantic lang '{lang}' is not found, see add new lang section in"
                f" griff/infrastructure/pydantic/locale/README.md"
            )
            raise typer.Exit()

    def _check_pot_filename_exists(self) -> Path:
        pot_filename = self._get_messages_filename()
        if pot_filename.exists():
            return pot_filename
        TyperPrint.error("locale is not initialized: run 'python commands locale init'")
        raise typer.Exit()
