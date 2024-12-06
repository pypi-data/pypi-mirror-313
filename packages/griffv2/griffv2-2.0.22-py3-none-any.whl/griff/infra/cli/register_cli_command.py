from types import FunctionType


def register_cli_command(name: str):
    def decorator(function: FunctionType):
        setattr(function, "_endpoint_name", name)
        return function

    return decorator
