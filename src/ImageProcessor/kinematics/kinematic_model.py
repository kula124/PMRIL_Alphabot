import configparser
from typing import Tuple
from simple_pid import PID

from math import atan2, pi, sqrt

from kinematics.kinematic_values import KinematicValues


class KinematicModel:
    def __init__(self, config: configparser.ConfigParser):
        self.__distance_margin = config.getfloat('distance_controller', 'margin')
        self.__current_goal: Tuple[int, int] = None

        self.__v_pid = PID(config.getfloat('angle_controller', 'k_P'), config.getfloat('angle_controller', 'k_I'),
                           config.getfloat('angle_controller', 'k_D'))
        self.__w_pid = PID(config.getfloat('angle_controller', 'k_P'), config.getfloat('angle_controller', 'k_I'),
                           config.getfloat('angle_controller', 'k_D'))

    def get_kinematic_values(self, trunk: Tuple[int, int], hood: Tuple[int, int],
                             goal: Tuple[int, int]) -> KinematicValues:

        if goal != self.__current_goal:
            self.__v_pid.reset()
            self.__w_pid.reset()
            self.__current_goal = goal

        robot = ((trunk[0] + hood[0]) / 2, (trunk[1] + hood[1]) / 2)

        delta_phi = self.get_angle_to_goal(goal, hood, robot, trunk)
        dist_to_goal = self.get_distance_to_goal(robot, goal)

        w = self.__w_pid(delta_phi)
        v = self.__v_pid(dist_to_goal)

        return KinematicValues(v, w)

    @staticmethod
    def get_angle_to_goal(goal, hood, robot, trunk):
        delta_phi = atan2(goal[1] - robot[1], goal[0] - robot[0])

        # Account for orientation
        if hood[1] < trunk[1]:
            delta_phi += pi + delta_phi
        return delta_phi

    def get_distance_to_goal(self, robot: Tuple[float, float], goal: Tuple[float, float]) -> float:
        dist_to_goal = sqrt((robot[0] - goal[0]) ** 2 + (robot[1] - goal[1]) ** 2)

        return 0 if dist_to_goal < self.__distance_margin else dist_to_goal
