import configparser
import struct
from typing import Tuple

from math import atan2, pi, sqrt

STRING_FORMAT = '{:.2f},{:.2f}'

class KinematicValues:
    def __init__(self, v: float, w: float):
        self.v = v
        self.w = w

    def as_ascii_bytes(self)->bytes:
        return STRING_FORMAT.format(self.v,self.w).encode(encoding="ASCII")

    def as_big_endian_bytes(self) -> bytearray:
        """
        First 4 bytes are v and last 4 are w
        :return: byte array representing speed and angular speed
        """
        return bytearray(struct.pack('!f', self.v)) + bytearray(struct.pack('!f', self.w))


class KinematicModel:
    def __init__(self, config: configparser.ConfigParser):
        self.__angle_kp = config.getfloat('angle_controller', 'k_P')
        self.__distance_margin = config.getfloat('distance_controller', 'margin')
        self.__distance_kp = config.getfloat('distance_controller', 'k_P')
        self.__current_goal: Tuple[int, int] = None

    def get_kinematic_values(self, trunk: Tuple[int, int], hood: Tuple[int, int],
                             goal: Tuple[int, int]) -> KinematicValues:

        robot = ((trunk[0] + hood[0]) / 2, (trunk[1] + hood[1]) / 2)

        delta_phi = atan2(goal[1] - robot[1], goal[0] - robot[0])

        # Account for orientation
        if hood[1] < trunk[1]:
            delta_phi += pi + delta_phi

        dist_to_goal = sqrt((robot[0] - goal[0]) ** 2 + (robot[1] - goal[1]) ** 2)
        if dist_to_goal < self.__distance_margin:
            dist_to_goal = 0

        w = self.__angle_kp * delta_phi
        v = self.__distance_kp * dist_to_goal if dist_to_goal >= self.__distance_margin else 0

        return KinematicValues(v, w)
