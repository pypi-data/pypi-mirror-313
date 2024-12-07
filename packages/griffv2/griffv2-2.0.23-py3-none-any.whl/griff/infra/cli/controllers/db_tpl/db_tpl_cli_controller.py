import subprocess

import typer
from injector import inject

from griff.infra.cli.controllers.abstract_db_cli_controller import (
    AbstractDbCliController,
)
from griff.infra.cli.register_cli_command import register_cli_command
from griff.infra.cli.typer_print import TyperPrint
from griff.services.path.path_service import PathService
from griff.settings.griff_settings import GriffSettings
from griff.utils.async_utils import AsyncUtils
from griff.utils.db_tpl_utils import DbTplUtils


class DbTplCliController(AbstractDbCliController):
    @inject
    def __init__(self, settings: GriffSettings):
        super().__init__(settings)

    def get_command_name(self):
        return "db_tpl"

    @register_cli_command(name="generate")
    def generate(self, context: str, noinput: bool = False):
        db_tpl = DbTplUtils(context, settings=self._settings)
        if AsyncUtils.async_to_sync(db_tpl.is_db_exists):
            if noinput is False:
                confirmed = typer.confirm(
                    f"It will regenerate current '{context}' template, are you sure?"
                )
                if not confirmed:
                    TyperPrint.warning("Ok, no pb, see you later !!")
                    raise typer.Exit()
            TyperPrint.info(f"Deleting Db template for context '{context}'")
            self._delete_tpl(db_tpl)
        TyperPrint.info(f"Creating Db template for context '{context}'")
        self._check_context_exists(db_tpl)
        TyperPrint.info("  creating db ...", with_newline=False)
        try:
            AsyncUtils.async_to_sync(db_tpl.create)
            TyperPrint.success(" OK")
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.info("  applying migration ...", with_newline=False)
        db_tpl.do_migration()
        TyperPrint.success(" OK")
        self._dump(db_tpl)
        TyperPrint.success("\nTemplate generated ! Ready to use (no need to init-tpl)")

    @register_cli_command(name="dump")
    def dump(self, context: str):
        TyperPrint.info(f"Dump Db template for context '{context}'")
        db_tpl = DbTplUtils(context, settings=self._settings)
        self._dump(db_tpl)
        TyperPrint.success("DONE")

    @register_cli_command(name="restore")
    def restore(self, context: str):
        TyperPrint.info(f"Restoring Db template for context '{context}'")
        db_tpl = DbTplUtils(context, settings=self._settings)
        AsyncUtils.async_to_sync(self._restore_db_tpl, db_tpl)
        TyperPrint.success("DONE")

    @register_cli_command(name="delete")
    def delete(self, context: str):
        db_tpl = DbTplUtils(context, settings=self._settings)
        TyperPrint.info(f"Delete Db template for context '{context}'")
        self._check_context_exists(db_tpl)
        self._delete_tpl(db_tpl)
        TyperPrint.success("DONE")

    @register_cli_command(name="migrate")
    def migrate(self, context: str = "all"):
        if context == "all":
            TyperPrint.info("Migrating All Db template")
            contexts = self._settings.bounded_contexts
        else:
            TyperPrint.info(f"Migrating Db template for context '{context}'")
            contexts = [context]

        for context in contexts:
            db_tpl = DbTplUtils(context, settings=self._settings)
            if db_tpl.dump_filename.exists():
                TyperPrint.info(
                    f"  applying migration for context '{context}'...",
                    with_newline=False,
                )
                db_tpl.do_migration()
                TyperPrint.success(" OK")
                self._dump(db_tpl)
            else:
                TyperPrint.warning(f"  no Db template found for context '{context}'")
        TyperPrint.success("DONE")

    def _check_context_exists(self, db_tpl: DbTplUtils):
        if db_tpl.is_context_exists():
            return None
        TyperPrint.error(f"context '{db_tpl.context}' not found")
        raise typer.Exit()

    def _dump(self, db_tpl: DbTplUtils):
        TyperPrint.info(
            f"  dumping db tpl {db_tpl.tpl_db_name} ...", with_newline=False
        )
        PathService().create_missing(db_tpl.dump_filename)
        p = subprocess.run(
            f"PGPASSWORD={self._settings.db.password} "
            f"pg_dump -Fc -Z 9 -U {self._settings.db.user} -h {self._settings.db.host} "
            f"-p {self._settings.db.port} "
            f"--file={db_tpl.dump_filename} {db_tpl.tpl_db_name}",
            shell=True,
        )
        self._check_process_run(p, "dump")
        db_tpl.dump_sql_filename.unlink(missing_ok=True)
        p = subprocess.run(
            f"PGPASSWORD={self._settings.db.password} "
            f"pg_dump --column-inserts "
            f"-U {self._settings.db.user} "
            f"-h {self._settings.db.host} "
            f"-p {self._settings.db.port} "
            f"--file={db_tpl.dump_sql_filename} {db_tpl.tpl_db_name}",
            shell=True,
        )
        self._check_process_run(p, "dump")
        TyperPrint.success(" OK")

    def _delete_tpl(self, db_tpl: DbTplUtils):
        TyperPrint.info("  deleting db ...", with_newline=False)
        try:
            AsyncUtils.async_to_sync(db_tpl.delete)
            TyperPrint.success(" OK")
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.info("  deleting dump ...", with_newline=False)
        db_tpl.dump_filename.unlink(missing_ok=True)
        db_tpl.dump_sql_filename.unlink(missing_ok=True)
        TyperPrint.success(" OK")
