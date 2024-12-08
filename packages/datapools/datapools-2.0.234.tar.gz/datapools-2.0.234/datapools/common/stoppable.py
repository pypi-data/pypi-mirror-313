import asyncio
from typing import Optional


class StoppableException(Exception):
    pass


class Stoppable:
    def __init__(self):
        self.stop_event = asyncio.Event()
        self.tasks = []
        self.is_running = False

    async def run(self):
        self.is_running = True

    async def stop(self):
        if not self.is_running:
            raise StoppableException("stop() before run()")

        self.stop_event.set()
        if len(self.tasks) > 0:
            await asyncio.wait(self.tasks, return_when=asyncio.ALL_COMPLETED)

    async def is_stopped(self, timeout: Optional[float] = None):
        if timeout is None:
            return self.stop_event.is_set()

        try:
            if hasattr(asyncio, "timeout"):
                async with asyncio.timeout(timeout):
                    await self.stop_event.wait()
                    return True
            else:
                await asyncio.wait_for(self.stop_event.wait(), timeout)
                return True
        except asyncio.TimeoutError:
            return False
