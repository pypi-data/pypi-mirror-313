import subprocess
from abc import abstractmethod

import typer
from asyncpg import InvalidCatalogNameError
from injector import inject

from griff.infra.cli.cli_controller import (
    CliController,
)
from griff.infra.cli.typer_print import TyperPrint
from griff.settings.griff_settings import GriffSettings
from griff.utils.db_tpl_utils import DbTplUtils


class AbstractDbCliController(CliController):
    @inject
    def __init__(self, settings: GriffSettings) -> None:
        self._settings = settings
        super().__init__()

    @abstractmethod
    def get_command_name(self) -> str:
        raise NotImplementedError

    async def _restore_db_tpl(self, db_tpl: DbTplUtils) -> None:
        TyperPrint.info(f"  restoring db {db_tpl.tpl_db_name} ...", with_newline=False)
        if db_tpl.dump_filename.exists() is False:
            TyperPrint.warning(" no db tpl found")
            return None

        try:
            await db_tpl.delete()
        except InvalidCatalogNameError:
            pass
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()

        try:
            await db_tpl.create()
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()

        if self._settings.env != "pytest":
            cmd = (
                f"PGPASSWORD={self._settings.db.password} "
                f"pg_restore -Fc -j 8 -U {self._settings.db.user} "
                f"-h {self._settings.db.host} "
                f"-p {self._settings.db.port} "
                f"-d {db_tpl.tpl_db_name} {db_tpl.dump_filename}"
            )
            p = subprocess.run(cmd, shell=True)  # noqa
            self._check_process_run(p, "restore")
        else:
            try:
                await db_tpl.restore_from_sql()
            except Exception as e:
                TyperPrint.error(f"  {e}")
                raise typer.Exit()

        TyperPrint.success(" OK")
