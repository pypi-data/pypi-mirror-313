from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import Protocol, runtime_checkable

from injector import Binder, Injector


def import_handlers(project_dir: str, event_handlers_dir: Path) -> None:
    skip_dirs = ["__pycache__", "_tests"]
    event_handler_files = [
        str(f)
        for f in event_handlers_dir.rglob("*.py")
        if set(f.parts).isdisjoint(skip_dirs) and not f.name.startswith("_")
    ]

    for file in event_handler_files:
        relative_path = file.replace(f"{str(project_dir)}/", "")
        module = relative_path.replace(".py", "").replace("/", ".")
        package = module.split(".")[-1].replace("_", " ").title().replace(" ", "")

        if module in globals() and hasattr(globals()[module], package):
            continue
        imported_module = import_module(module)
        if hasattr(imported_module, package):
            globals().update({package: getattr(imported_module, package)})
            continue
        raise RuntimeError(f"package {package} not found in {module}")
    return None


@runtime_checkable
class Runnable(Protocol):
    @abstractmethod
    def initialize(self, injector: Injector) -> None:
        ...

    @abstractmethod
    def start(self, injector: Injector) -> None:
        ...

    @abstractmethod
    def stop(self, injector: Injector) -> None:
        ...

    @abstractmethod
    def clean(self, injector: Injector) -> None:
        ...


@runtime_checkable
class AsyncRunnable(Protocol):
    @abstractmethod
    async def async_start(self, injector: Injector) -> None:
        ...

    @abstractmethod
    async def async_stop(self, injector: Injector) -> None:
        ...


@runtime_checkable
class InjectBindable(Protocol):
    @abstractmethod
    def configure(self, binder: Binder) -> None:
        ...


class RuntimeComponent(ABC):
    def __str__(self) -> str:
        return self.__class__.__name__
