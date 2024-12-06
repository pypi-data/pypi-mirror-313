import datetime
import inspect
import json
import logging
import os
import subprocess
import tempfile
from abc import ABC
from copy import copy
from decimal import Decimal
from pathlib import Path
from shutil import rmtree
from typing import Any

from pydantic import BaseModel, ValidationError

from griff.services.path.path_service import PathService

logger = logging.getLogger(__name__)


class AbstractTestCase(ABC):  # pragma: no cover
    _base_dir = None
    _base_test_dir = "/_tests"
    _fixture_dir = None
    _common_fixture_dir = None

    @classmethod
    def setup_class(cls) -> None:
        if hasattr(super(), "setup_class"):
            raise RuntimeError("Must be the last class in the inheritance chain")
        cls.clean_sandbox()
        cls.read_file = PathService().read_file  # type: ignore

    def setup_method(self) -> None:
        if hasattr(super(), "setup_method"):
            raise RuntimeError("Must be the last class in the inheritance chain")

    @classmethod
    def teardown_class(cls) -> None:
        pass

    def teardown_method(self) -> None:
        pass

    @classmethod
    def get_dataset(cls, dataset) -> Any:
        """
        Get fixture dataset if is json, load it else just read it
        Args:
            dataset(str): relative path to dataset directory
        Returns:
            mixed
        """
        return cls._get_dataset(dataset, cls.get_datasets_dir(dataset))

    @classmethod
    def get_datasets_dir(cls, relative_path=None) -> str:
        dir = f"{cls._get_test_fixtures_dir()}/datasets"
        if relative_path:
            return f"{dir}/{relative_path}"
        return dir

    def assert_equals_resultset(self, actual, **kwargs):
        # build resultset filename from caller filename
        calling_filename = kwargs.get("calling_filename", None)
        filename = self._get_calling_filename()
        calling_frame = self._get_calframe(calling_filename)
        method_name = self._get_calling_method_name(calling_frame)
        sub_dir = self._get_test_subdir(filename)
        filename_noext = Path(filename).name.replace(".py", "")
        resultset_filename = Path(
            f"{self._get_resultsets_dir()}/{sub_dir}/{filename_noext}"
            f"/{method_name}.json"
        )
        self._create_missing_directories(resultset_filename)

        actual_json = self._json_dump(actual)

        # get expected result sets from file
        if resultset_filename.exists() is False:
            # create missing file
            data = (
                actual_json
                if os.environ.get("TEST_RESULTSET_AUTOSAVE", False)
                else "{}"
            )
            with resultset_filename.open("w") as f:
                f.write(data)

        with resultset_filename.open() as json_file:
            expected = json_file.read()

        # assert

        try:
            assert expected == actual_json
        except AssertionError as e:
            tmp_dir = self._get_tmp_dir()

            # build fix result set
            tmp_actual_filename = Path(
                f"{tmp_dir}/{filename_noext}-{method_name}_ACTUAL.json"
            )
            self._create_missing_directories(tmp_actual_filename)

            with tmp_actual_filename.open("w") as f:
                f.write(actual_json)

            default_diff_tool = os.getenv("DEFAULT_TU_DIFF_TOOL", None)
            if default_diff_tool:
                diff_cmd = default_diff_tool.replace(
                    "__expected__", str(resultset_filename)
                ).replace("__actual__", str(tmp_actual_filename))
                # noinspection SubprocessShellMode
                subprocess.Popen(diff_cmd, shell=True)
            else:
                logger.warning(
                    "No diff tool configured, add to your .env: "
                    'DEFAULT_TU_DIFF_TOOL="charm diff __expected__ __actual__"'
                )

            print(f"\n\033[1;31m=== TEST {method_name} has failed !!")
            print(f"file: {filename}")
            os.system(f"diff {resultset_filename} {tmp_actual_filename}")
            print(f"=== TEST {method_name}\n\033[0m")
            raise e

    @classmethod
    def clean_sandbox(cls):
        cls._empty_dir(cls._get_base_sandbox_dir())

    @classmethod
    def get_sandbox_dir(cls, filename=None) -> str:
        sandbox_path = cls._get_base_sandbox_dir().joinpath(cls.__name__)
        if filename is None:
            sandbox_path.mkdir(parents=True, exist_ok=True)
            return str(sandbox_path)
        filename = Path(f"{sandbox_path}/{filename}")
        cls._create_missing_directories(filename)
        return str(filename)

    @staticmethod
    def assert_path_exists(path):
        assert os.path.exists(path), path

    @staticmethod
    def assert_path_not_exists(path):
        assert not os.path.exists(path), path

    @classmethod
    def _empty_dir(cls, directory: Path) -> None:
        full_path = Path(directory)
        if full_path.exists():
            rmtree(full_path)
            full_path.mkdir()

    @classmethod
    def _get_dataset(cls, dataset: str, dataset_filename: str) -> Any:
        filename, file_extension = os.path.splitext(dataset)
        with open(dataset_filename) as file:
            if file_extension == ".json":
                data = json.load(file)
                if "__generated_by__" in dataset:
                    data.pop("__generated_by__")
                return data
            return file.read()

    @classmethod
    def _get_tmp_dir(cls) -> str:
        """Get tmp test directory"""
        return f"{tempfile.tempdir}/.donotcommit_tmp"

    @classmethod
    def _get_test_fixtures_dir(cls) -> str:
        """
        Get fixtures directory

        Returns:
            str: fixtures directory
        """
        if not cls._fixture_dir:
            filename = cls._get_calling_filename()
            pos = filename.find(cls._base_test_dir)
            if not pos > 0:
                raise ValueError(f"Unable to determine root tests path from {filename}")
            cls._fixture_dir = f"{filename[:pos]}{cls._base_test_dir}/_fixtures"

        return cls._fixture_dir

    @classmethod
    def _get_resultsets_dir(cls) -> str:
        """
        Get result sets dir

        Returns:
            str: result sets directory
        """
        return f"{cls._get_test_fixtures_dir()}/resultsets"

    @classmethod
    def _get_base_sandbox_dir(cls):
        return Path(f"{cls._get_test_fixtures_dir()}/sandbox")

    @classmethod
    def _get_calling_filename(cls) -> str:
        return inspect.getfile(cls)

    @classmethod
    def _get_calframe(cls, calling_filename=None) -> inspect.FrameInfo:
        # find calling frame
        calframe = inspect.getouterframes(inspect.currentframe(), 2)
        test_filename = (
            cls._get_calling_filename() if not calling_filename else calling_filename
        )
        for frame in calframe:
            if frame.filename.find(test_filename) >= 0:
                return frame
        raise ValueError("Unable to determine calling frame")

    @staticmethod
    def _get_calling_method_name(frame) -> Any:
        return frame[3]

    @staticmethod
    def _get_calling_lineno(frame) -> str:
        return frame.lineno

    @staticmethod
    def _create_missing_directories(filename: Path) -> None:
        if filename.exists():
            return None

        filename = filename.parent
        filename.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_test_subdir(cls, filename):
        dir_names = str(Path(filename).parent).split("/")

        # search tests dir
        for _ in range(0, len(dir_names)):
            dir_name = dir_names.pop(0)
            if dir_name == "_tests":
                break

        return "/".join(dir_names)

    @classmethod
    def _json_dump(cls, data):
        json_dump = json.dumps(
            cls._to_json_dumpable(data),
            indent=4,
            separators=(",", ": "),
            default=str,
            # disable non-ASCII characters escape with \uXXXX sequences
            ensure_ascii=False,
        )
        # for respecting file empty last line convention
        return f"{json_dump}\n"

    @classmethod
    def _to_json_dumpable(cls, data):
        """
        Convert data to be json dumpable
        """
        dumpable_data = copy(data)
        if isinstance(dumpable_data, BaseModel):
            dumpable_data = dumpable_data.model_dump()

        if isinstance(dumpable_data, tuple):
            dumpable_data = list(dumpable_data)

        if isinstance(dumpable_data, dict):
            jsonized = {}
            for k, v in dumpable_data.items():
                new_k = cls._to_json_dumpable(k)
                jsonized[new_k] = cls._to_json_dumpable(v)
            return jsonized

        if isinstance(dumpable_data, list):
            for i, v in enumerate(dumpable_data):
                dumpable_data[i] = cls._to_json_dumpable(v)
            return dumpable_data

        if isinstance(dumpable_data, set):
            dumpable_data = cls._to_json_dumpable(list(dumpable_data))

        if isinstance(dumpable_data, Decimal):
            return float(dumpable_data)

        # if isinstance(prepared_data, Arrow):
        #     return prepared_data.format()

        if isinstance(dumpable_data, datetime.datetime):
            return dumpable_data.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(dumpable_data, datetime.date):
            return dumpable_data.strftime("%Y-%m-%d")

        if isinstance(dumpable_data, ValidationError):
            return cls._to_json_dumpable(dumpable_data.errors(include_url=False))

        return dumpable_data
