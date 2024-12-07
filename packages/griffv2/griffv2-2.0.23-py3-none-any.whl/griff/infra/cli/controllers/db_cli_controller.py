import os

import typer
from injector import inject

from griff.infra.cli.controllers.abstract_db_cli_controller import (
    AbstractDbCliController,
)
from griff.infra.cli.register_cli_command import register_cli_command
from griff.infra.cli.typer_print import TyperPrint
from griff.services.db.providers.asyncpg_provider import AsyncPgProvider
from griff.services.path.path_service import PathService
from griff.settings.griff_settings import GriffSettings
from griff.utils.async_utils import AsyncUtils
from griff.utils.db_tpl_utils import DbTplUtils
from griff.utils.migration_utils import MigrationUtils


class DbCliController(AbstractDbCliController):
    @inject
    def __init__(self, settings: GriffSettings, path_service: PathService):
        super().__init__(settings)
        self._path_service = path_service

    def get_command_name(self):
        return "db"

    def _get_migrations_dir(self, domain_name: str) -> str:
        return str(self._settings.get_migrations_path(domain_name))

    @register_cli_command(name="init-bdd")
    def initialize_bdd(self, noinput: bool = False):
        if noinput is False:
            confirmed = typer.confirm(
                f"It will erase entire database "
                f"'{self._settings.db.name}', are you sure?"
            )
            if not confirmed:
                TyperPrint.warning("Ok, no pb, see you later !!")
                raise typer.Exit()
        TyperPrint.info("Init Bdd")

        AsyncUtils.async_to_sync(self._recreate_db)

        self._do_migrations()

        if self._settings.env in ["dev", "pytest"]:
            AsyncUtils.async_to_sync(self._recreate_db, True)
            self.initialize_db_tpl()

    @register_cli_command(name="init-tpl")
    def initialize_db_tpl(self):
        if self._settings.env not in ["dev", "pytest"]:
            TyperPrint.error(f"command forbidden in '{self._settings.env}' environment")
            raise typer.Exit()
        TyperPrint.info("Init Db Templates")
        AsyncUtils.async_to_sync(self._recreate_db_tpl)

    @register_cli_command(name="migrate")
    def migrate(self):
        self._do_migrations()

    @register_cli_command(name="makemigrations")
    def make_migrations(self, domain_name: str, migration_name: str):
        migration_dir = self._get_migrations_dir(domain_name)
        self._path_service.create_missing(migration_dir)
        os.system(f"yoyo new --sql {migration_dir}" f" -m '{migration_name}'")

    async def _recreate_db(self, db_test=False):
        db_name = (
            self._settings.db.name if not db_test else self._settings.db.db_test_name
        )
        settings = self._settings.db.model_copy(deep=True, update={"name": "template1"})
        provider = AsyncPgProvider(settings)
        async with provider.connection() as conn:
            await provider.disconnect_all(conn)
            # noinspection TryExceptPass,PyBroadException
            try:
                await self._drop_db(conn, db_name)
            except Exception:
                pass
            await self._create_db(conn, db_name)

    async def _recreate_db_tpl(self):
        for context in self._settings.bounded_contexts:
            await self._restore_db_tpl(DbTplUtils(context, self._settings))

    @staticmethod
    async def _create_db(conn, db_name):
        TyperPrint.info(f"  creating db '{db_name}' ...", with_newline=False)
        try:
            # noinspection SqlInjection
            sql = f"CREATE DATABASE {db_name}"
            await conn.execute(sql)
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.success(" OK")

    @staticmethod
    async def _drop_db(conn, db_name):
        TyperPrint.info(f"  droping db '{db_name}' ...", with_newline=False)
        try:
            # noinspection SqlInjection
            sql = f"DROP DATABASE {db_name}"
            await conn.execute(sql)
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.success(" OK")

    def _do_migrations(self):
        for context in self._settings.bounded_contexts:
            self._migrate_context(context)

    def _migrate_context(self, context):
        migrations_path = str(self._settings.get_migrations_path(context))
        TyperPrint.info(
            f"  applying migration(s) for {context} ...", with_newline=False
        )
        MigrationUtils.migrate(self._settings.db.dsn, migrations_path)
        TyperPrint.success(" OK")
