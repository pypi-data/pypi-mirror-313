import asyncio
import os
import random

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class FakeLagTimeMiddleware(BaseHTTPMiddleware):  # pragma: no cover
    """
    simulate response lag
    """

    def __init__(self, app):
        super().__init__(app)
        self._durations = [0, 0.3, 0.5, 0.5, 0.5, 0.5, 0.6, 0.8, 0.8, 1]
        self._is_active = bool(os.getenv("API_FAKE_LAG_TIME", default=0))

    async def dispatch(self, request, call_next):
        # Proceed with the request
        response = await call_next(request)
        if self._is_active:
            await self.simulate_lagtime()
        return response

    async def simulate_lagtime(self):
        sleep_duration = random.choice(self._durations)
        if sleep_duration > 0:
            logger.info(f"Fake lag time of {sleep_duration}s ...")
            await asyncio.sleep(sleep_duration)
            logger.info("Fake lag time over")
        else:
            logger.info("Fake lag ignored")
