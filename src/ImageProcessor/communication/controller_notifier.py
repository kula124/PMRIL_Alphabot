import configparser
import serial


class ControllerNotifier:
    def __init__(self, config: configparser.ConfigParser):
        self.__serial_port = f'/dev/{config.get("communication", "port")}'
        self.__baudrate = config.getint('communication', 'baudrate')
        # noinspection PyUnresolvedReferences
        # Serial is dynamically assigned depending on the current platform
        self.__serial = serial.Serial(self.__serial_port, baudrate=self.__baudrate)

    def notify(self, data: bytearray) -> None:
        self.__serial.write(data)

    def dispose(self) -> None:
        self.__serial.close()
