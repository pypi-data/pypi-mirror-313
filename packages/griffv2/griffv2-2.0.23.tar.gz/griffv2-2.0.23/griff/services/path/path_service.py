import shutil
from pathlib import Path

from griff.services.abstract_service import AbstractService
from griff.utils import exceptions


class PathService(AbstractService):
    def check_exists(self, path: str | Path) -> Path:
        path_path = self.to_path(path)
        if path_path.exists():
            return path_path
        raise exceptions.NotFoundException(f"'{path}' does not exist")

    def create_missing(self, path: str | Path) -> None:
        """
        create missing directories for directory or path
        """
        path_path = self.to_path(path)
        if path_path.suffix:
            path_path = path_path.parent
        path_path.mkdir(parents=True, exist_ok=True)

    def read_file(self, filename: str | Path) -> str:
        filename_path = self.check_exists(filename)
        with filename_path.open("r") as fd:
            return fd.read()

    def write_file(self, filename: str | Path, content: str) -> None:
        filename_path = self.to_path(filename)
        self.check_exists(filename_path.parent)
        with filename_path.open("w") as f:
            f.write(content)

    @staticmethod
    def copy_file(src: str | Path, dst: str | Path):
        shutil.copy(str(src), str(dst))

    @staticmethod
    def to_path(path) -> Path:
        """Get Path instance if path is not"""
        if isinstance(path, Path):
            return path
        return Path(path)
