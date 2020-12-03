import configparser
import queue

import websockets

from utils.async_event_loop_thread import AsyncEventLoopThread


class ControllerNotifier:
    def __init__(self, config: configparser.ConfigParser):
        self.__server_uri = config['communication']['server_uri']
        self.__queue = queue.Queue()

        self.__worker_thread = AsyncEventLoopThread()
        self.__worker_thread.start()
        self.__worker_thread.run_coroutine(self.websocket_client_loop())

    def notify(self, json_data: str) -> None:
        self.__queue.put(json_data)

    async def websocket_client_loop(self):
        async with websockets.connect(self.__server_uri) as ws:
            while True:
                # This is blocking get but we don't care because this does not run in the main thread.
                data = self.__queue.get()
                await ws.send(data)
