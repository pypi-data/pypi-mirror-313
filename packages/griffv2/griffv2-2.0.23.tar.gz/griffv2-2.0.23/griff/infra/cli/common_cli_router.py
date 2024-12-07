from injector import inject, singleton

from griff.infra.cli.cli_router import CliRouter
from griff.infra.cli.controllers.db_cli_controller import DbCliController
from griff.infra.cli.controllers.db_tpl.db_tpl_cli_controller import (
    DbTplCliController,
)
from griff.infra.cli.controllers.i18n_cli_controller import I18nCliController


@singleton
class CommonCliRouter(CliRouter):
    @inject
    def __init__(
        self,
        i18n: I18nCliController,
        db_tpl_ctrl: DbTplCliController,
        db_contrl: DbCliController,
    ):
        super().__init__()
        self._app.add_typer(i18n.get_app(), name=i18n.get_command_name())
        self._app.add_typer(db_tpl_ctrl.get_app(), name=db_tpl_ctrl.get_command_name())
        self._app.add_typer(db_contrl.get_app(), name=db_contrl.get_command_name())

    def get_command_group_name(self) -> str:
        return "common"
