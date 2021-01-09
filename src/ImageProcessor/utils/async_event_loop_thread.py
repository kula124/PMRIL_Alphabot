import asyncio
import threading
from concurrent import futures


class AsyncEventLoopThread(threading.Thread):
    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__loop = loop or asyncio.new_event_loop()
        self.__running = False
        self.name = 'EventLoopThread'

    def run(self) -> None:
        self.__running = True
        self.__loop.run_forever()

    def run_coroutine(self, coroutine) -> futures.Future:
        return asyncio.run_coroutine_threadsafe(coroutine, loop=self.__loop)

    def stop(self) -> None:
        if self.__running:
            self.__loop.call_soon_threadsafe(self.__loop.stop)
            self.join()
            self.__running = False
