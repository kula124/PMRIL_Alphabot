import configparser
import queue

import websockets

from utils.async_event_loop_thread import AsyncEventLoopThread
from utils.logger_factory import get_logger


class ControllerNotifier:
    def __init__(self, config: configparser.ConfigParser):
        self.__logger = get_logger()
        self.__server_uri = config['communication']['server_uri']
        self.__queue = queue.Queue()

        self.__worker_thread = AsyncEventLoopThread()
        self.__worker_thread.start()
        self.__worker_thread.run_coroutine(self.websocket_client_loop())

    def notify(self, json_data: str) -> None:
        self.__queue.put(json_data)

    async def websocket_client_loop(self):
        try:
            async with websockets.connect(self.__server_uri) as ws:
                while True:
                    # This is blocking get but we don't care because this does not run in the main thread.
                    data = self.__queue.get()
                    self.__logger.debug('Sending data to the server...')
                    await ws.send(data)
                    self.__logger.debug('Successfully sent data to the server!')
        except websockets.ConnectionClosed as e:
            self.__logger.error(f'Something went wrong: {e.reason}')
            raise e
        except Exception as e:
            self.__logger.error(f'Something went terribly wrong: {e}')
            raise e
        finally:
            self.__worker_thread.stop()

    def dispose(self):
        self.__worker_thread.stop()
