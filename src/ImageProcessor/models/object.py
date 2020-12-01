from typing import Tuple

DEFAULT_OBJECT_COLOR = (0, 255, 0)


class Object:
    def __init__(self, label=None, x=None, y=None, color=None):
        self.__set_label(label if label else 'Object')
        self.__set_color(color if color else DEFAULT_OBJECT_COLOR)
        self.__set_x_pos(x if x else 0)
        self.__set_y_pos(y if y else 0)
        self.__set_hsv_max((0, 0, 0))
        self.__set_hsv_min((0, 0, 0))

    @staticmethod
    def red():
        red = Object('Red')
        red.__set_color((0, 0, 255))
        red.__set_hsv_min((0, 200, 0))
        red.__set_hsv_max((19, 255, 255))

        return red

    @staticmethod
    def blue():
        blue = Object('Blue')
        blue.__set_color((255, 0, 0))
        blue.__set_hsv_min((92, 0, 0))
        blue.__set_hsv_max((124, 255, 255))

        return blue

    @staticmethod
    def green():
        green = Object('Green')
        green.__set_color((0, 255, 0))
        green.__set_hsv_min((34, 50, 50))
        green.__set_hsv_max((80, 220, 200))

        return green

    @staticmethod
    def yellow():
        yellow = Object('Yellow')
        yellow.__set_color((0, 255, 255))
        yellow.__set_hsv_min((20, 124, 123))
        yellow.__set_hsv_max((30, 255, 255))

        return yellow

    def __set_color(self, color: Tuple[int, int, int]) -> None:
        self.__color = color

    def get_color(self) -> Tuple[int, int, int]:
        return self.__color

    def __set_label(self, label: str) -> None:
        self.__label = label

    def get_label(self) -> str:
        return self.__label

    def __set_x_pos(self, x_pos: int) -> None:
        self.__x_pos = x_pos

    def get_x_pos(self) -> int:
        return self.__x_pos

    def __set_y_pos(self, y_pos: int) -> None:
        self.__y_pos = y_pos

    def get_y_pos(self) -> int:
        return self.__y_pos

    def __set_hsv_min(self, hsv_min: Tuple[int, int, int]) -> None:
        self.__hsv_min = hsv_min

    def get_hsv_min(self) -> Tuple[int, int, int]:
        return self.__hsv_min

    def __set_hsv_max(self, hsv_max: Tuple[int, int, int]) -> None:
        self.__hsv_max = hsv_max

    def get_hsv_max(self) -> Tuple[int, int, int]:
        return self.__hsv_max
