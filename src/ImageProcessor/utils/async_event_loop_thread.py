import asyncio
import threading
from concurrent import futures


class AsyncEventLoopThread(threading.Thread):
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop or asyncio.new_event_loop()
        self.running = False

    def run(self) -> None:
        self.running = True
        self.loop.run_forever()

    def run_coroutine(self, coroutine) -> futures.Future:
        return asyncio.run_coroutine_threadsafe(coroutine, loop=self.loop)

    def stop(self) -> None:
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join()
        self.running = False
