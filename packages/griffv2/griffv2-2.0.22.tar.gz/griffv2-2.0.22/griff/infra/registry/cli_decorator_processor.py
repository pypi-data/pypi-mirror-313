from typing import Dict


class CliDecoratorProcessor:
    def __init__(self) -> None:
        self._name: str | None = None

    def _sanitize(self, to_be_sanitized: str) -> str:
        return to_be_sanitized.strip("'").strip('"').strip(" ")

    def _process_name_param(self, a_str_to_process: str) -> None:
        splited = a_str_to_process.split("=")
        self._name = self._sanitize(splited[1])

    def load_decorators(self, a_decoration_string_list: list[str]) -> None:
        for decorator in a_decoration_string_list:
            if decorator[:21] == "@register_cli_command":
                keyval_list = decorator[
                    decorator.index("(") + 1 : decorator.index(")")  # noqa: E203
                ].split(",")
                for decoration_param in keyval_list:
                    if "=" not in decoration_param:
                        raise ValueError("decoration badly formatted, '=' not found")
                    self._process_name_param(a_str_to_process=decoration_param)

    def get_decorator_params(self) -> Dict[str, str | None]:
        return {"name": self._name}

    @property
    def name(self) -> str | None:
        return self._name
