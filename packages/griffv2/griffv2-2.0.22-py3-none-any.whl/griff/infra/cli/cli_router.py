from abc import ABC, abstractmethod

import typer
from typer import Typer

from griff.infra.registry.meta_registry import MetaCliRouterRegistry


class CliRouter(ABC, metaclass=MetaCliRouterRegistry):
    def __init__(self):
        self._app = typer.Typer()

    def get_app(self) -> Typer:
        return self._app

    @abstractmethod
    def get_command_group_name(self) -> str:
        raise NotImplementedError
