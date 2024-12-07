import functools


# noinspection PyPep8Naming
class register_endpoint:
    def __init__(self, route=None, method=None, success_code=None):
        self.route = route
        self.method = method

    def __call__(self, func):
        """Calling the class."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):  # pragma: no cover
            value = await func(*args, **kwargs)
            return value

        return wrapper
