import asyncio
import configparser
import queue

import websockets

from utils.async_event_loop_thread import AsyncEventLoopThread
from utils.logger_factory import get_logger


class ControllerNotifier:
    def __init__(self, config: configparser.ConfigParser):
        self.__logger = get_logger()
        self.__server_uri = config['communication']['server_uri']
        self.__poll_interval = config.getfloat('communication', 'poll_interval_in_ms') / 1000
        self.__queue = queue.Queue()
        self.exc_info = None

        self.__worker_thread = AsyncEventLoopThread()
        self.__worker_thread.start()
        self.__worker_thread.run_coroutine(self.websocket_client_loop())

    def notify(self, json_data: str) -> None:
        self.__queue.put(json_data)

    async def websocket_client_loop(self):
        try:
            async with websockets.connect(self.__server_uri) as ws:
                while True:
                    try:
                        data = self.__queue.get_nowait()
                        self.__logger.debug('Sending data to the server...')
                        await ws.send(data)
                        self.__logger.debug('Successfully sent data to the server!')
                    except queue.Empty:
                        await asyncio.sleep(self.__poll_interval)

        except websockets.ConnectionClosed as e:
            self.__logger.error(f'Connection was closed with reason: {e.reason}')
            import sys
            self.exc_info = sys.exc_info()
        except Exception as e:
            self.__logger.error(f'Something went terribly wrong: {e}')
            import sys
            self.exc_info = sys.exc_info()
        finally:
            self.dispose()

    def dispose(self):
        self.__worker_thread.stop()
