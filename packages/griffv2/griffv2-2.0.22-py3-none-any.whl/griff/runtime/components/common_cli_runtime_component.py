from injector import Injector, Binder, singleton
from typer import Typer

from griff.infra.cli.common_cli_router import CommonCliRouter
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
)


class CommonCliRuntimeComponent(InjectBindable, Runnable, RuntimeComponent):
    def configure(self, binder: Binder) -> None:
        binder.bind(Typer, to=Typer, scope=singleton)

    def initialize(self, injector: Injector):
        typer = injector.get(Typer)
        cli_router = injector.get(CommonCliRouter)
        typer.add_typer(cli_router.get_app(), name=cli_router.get_command_group_name())

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass
