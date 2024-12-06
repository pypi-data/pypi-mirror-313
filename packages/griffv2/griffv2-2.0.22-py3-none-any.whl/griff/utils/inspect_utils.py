import inspect
from typing import List, Callable, Any


def get_decorators(function: Callable[[Any], Any]) -> List[str]:
    """Returns list of decorators names

    Args:
        function (Callable): decorated method/function

    Return:
        List of decorators as strings

    Example:
        Given:

        @my_decorator
        @another_decorator
        def decorated_function():
            pass

        >> get_decorators(decorated_function)
        ['@my_decorator', '@another_decorator']

    """
    source = inspect.getsource(function)
    if "@" not in source:
        return []
    source = source.replace("\n", "")
    index = source.find("def ")
    async_index = source.find("async ")
    if index > async_index != -1:
        index = async_index
    return [
        f"@{line.replace(' ', '')}"
        for line in source[:index].strip().split("@")
        if line != ""
    ]


def find_bound_method_to_object(obj: object, method_name: str) -> Any:
    members = inspect.getmembers(obj)
    return [mem for mem in members if mem[0] == method_name][0][1]
