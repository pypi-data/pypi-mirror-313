import asyncio
from typing import Any, Callable


class AsyncUtils:
    @staticmethod
    def async_to_sync(async_func: Callable, args: object = None) -> Any:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:  # pragma: no cover
            loop = asyncio.new_event_loop()

        if isinstance(args, dict):  # pragma: no cover
            coroutine = async_func(**args) if args else async_func()
        elif isinstance(args, list):  # pragma: no cover
            coroutine = async_func(*args) if args else async_func()
        else:
            coroutine = async_func(args) if args else async_func()

        return loop.run_until_complete(coroutine)
