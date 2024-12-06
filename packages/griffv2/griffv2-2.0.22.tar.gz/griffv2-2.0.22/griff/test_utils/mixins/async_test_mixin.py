import pytest_asyncio

from griff.utils.async_utils import AsyncUtils


class AsyncTestMixin(AsyncUtils):
    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def _async_setup_teardown_class(self):
        await self.async_setup_class()
        yield
        await self.async_teardown_class()

    async def async_setup_class(self):
        # ATTENTION le self reçu sera différent de celui async_setup et donc du test
        # => tout attribut affecté ici ne le sera pas dans le context du test
        pass

    async def async_teardown_class(self):
        pass

    @pytest_asyncio.fixture(autouse=True)
    async def _async_setup_teardown_method(self):
        await self.async_setup()
        yield
        await self.async_teardown()

    async def async_setup(self):
        pass

    async def async_teardown(self):
        pass
