import asyncio
import configparser
import queue

import serial

from utils import logger_factory
from utils.async_event_loop_thread import AsyncEventLoopThread


class ControllerNotifier:
    def __init__(self, config: configparser.ConfigParser):
        self.__logger = logger_factory.get_logger()

        self.__serial_port = f'/dev/{config.get("communication", "port")}'
        self.__baudrate = config.getint('communication', 'baudrate')
        self.__poll_interval = config.getfloat('communication', 'poll_interval_in_ms') / 1000

        self.__queue = queue.Queue()
        self.exc_info = None

        self.__worker_thread = AsyncEventLoopThread()
        self.__worker_thread.start()
        self.__worker_thread.run_coroutine(self.serial_client_loop())

    def notify(self, data: bytearray) -> None:
        self.__queue.put(data)

    async def serial_client_loop(self):
        try:
            # noinspection PyUnresolvedReferences
            # Serial is dynamically assigned depending on the current platform
            with serial.Serial(self.__serial_port, baudrate=self.__baudrate) as ser:
                while True:
                    try:
                        data = self.__queue.get_nowait()
                        self.__logger.debug('Sending data to the robot...')
                        ser.write(data)
                        self.__logger.debug('Successfully sent data to the robot!')
                    except queue.Empty:
                        await asyncio.sleep(self.__poll_interval)

        except Exception as e:
            self.__logger.error(f'Something went terribly wrong: {e}')
            import sys
            self.exc_info = sys.exc_info()

        finally:
            self.dispose()

    def dispose(self) -> None:
        self.__worker_thread.stop()
