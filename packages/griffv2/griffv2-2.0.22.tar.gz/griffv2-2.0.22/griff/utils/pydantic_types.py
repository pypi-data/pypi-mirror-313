from gettext import gettext as _
from pathlib import Path

from pydantic import (
    AfterValidator,
    StringConstraints,
)
from typing_extensions import Annotated


def _check_is_relative_path(path: Path) -> Path:
    if path.exists():
        raise ValueError(_("'%(path)s' is not a relative path") % {"path": path})
    return path


def validate_is_relative_path(v: str) -> str:
    return str(_check_is_relative_path(Path(v)))


def validate_is_relative_dest_path(v: Path) -> Path:
    path = Path(v)
    validate_is_relative_path(str(path.parent))
    return v


def validate_path_exists(v: str) -> str:
    if Path(v).exists():
        return v
    raise ValueError(_("'%(path)s' not found") % {"path": v})


def validate_dest_filename_exists(v: str) -> str:
    path = Path(v)
    validate_path_exists(str(path.parent))
    return v


# String
NoEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

# Path
FilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_path_exists)]
DirectoryStr = FilenameStr
DestFilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_dest_filename_exists)]
RelativeDirectoryStr = Annotated[NoEmptyStr, AfterValidator(validate_is_relative_path)]
RelativeFilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_is_relative_path)]
RelativeDestFilenameStr = Annotated[
    NoEmptyStr, AfterValidator(validate_is_relative_dest_path)
]
