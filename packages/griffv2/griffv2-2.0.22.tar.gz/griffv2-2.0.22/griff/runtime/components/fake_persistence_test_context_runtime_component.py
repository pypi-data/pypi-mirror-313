import ast
import glob
import importlib.util
from pathlib import Path

from injector import Binder

from griff.runtime.components.abstract_runtime_component import (
    InjectBindable,
    RuntimeComponent,
)
from griff.settings.griff_settings import GriffSettings


def get_classes_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        root = ast.parse(file.read())

    classes = [node.name for node in ast.walk(root) if isinstance(node, ast.ClassDef)]
    return classes


def scan_persistence_classes(directory, type_name: str):
    python_classes = []

    for filepath in glob.glob(f"{directory}/*_{type_name}.py", recursive=True):
        classes = get_classes_from_file(filepath)
        if classes:
            class1, class2 = classes
            python_classes.append(
                {
                    "module": str(Path(filepath).name)[:-3],
                    "real": class1 if "Fake" not in class1 else class2,
                    "fake": class1 if "Fake" in class1 else class2,
                }
            )
    return python_classes


class FakePersistenceTestContextRuntimeComponent(InjectBindable, RuntimeComponent):
    def __init__(self, context: str, settings: GriffSettings):
        self.base_module = str(
            settings.get_repositories_path(context=context, absolute=False)
        ).replace("/", ".")
        self.repository_path = settings.get_repositories_path(context=context)

    def configure(self, binder: Binder) -> None:
        self._bind_fake_classes(binder, type_name="persistence")
        self._bind_fake_classes(binder, type_name="repository")

    def _bind_fake_classes(self, binder: Binder, type_name: str):
        for klasses in scan_persistence_classes(self.repository_path, type_name):
            real_klass, fake_klass = self._import_module(klasses)
            binder.bind(real_klass, to=fake_klass)

    def _import_module(self, klasses: dict):
        module_name = f"{self.base_module}.{klasses['module']}"
        imported_module = importlib.import_module(module_name)
        for klass in [klasses["real"], klasses["fake"]]:
            if module_name in globals() and hasattr(globals()[module_name], klass):
                continue
            if hasattr(imported_module, klass) is False:
                raise RuntimeError(f"package {klass} not found in {module_name}")
            globals().update({klass: getattr(imported_module, klass)})
        return getattr(imported_module, klasses["real"]), getattr(
            imported_module, klasses["fake"]
        )
