import configparser
from typing import List, Tuple

from communication.controller_notifier import ControllerNotifier
from kinematics.kinematic_model import KinematicModel, KinematicValues
from models.object import Object
from models.sample import Sample
from models.vehicle_enum import VehiclePart
from utils.logger_factory import get_logger


class CommunicationManager:
    def __init__(self, config: configparser.ConfigParser):
        self.__logger = get_logger()
        self.__config = config
        self.__sample_count = self.__config.getint('communication', 'sample_count')
        self.__trunk_sample_count = 0
        self.__hood_sample_count = 0
        self.__samples: List[Sample] = []
        self.__target_coordinates = None
        self.__kinematic_model = KinematicModel(config)
        self.__controller_notifier = ControllerNotifier(config)

    def handle(self, filtered_objects: List[Object], target: Tuple[int, int]) -> None:
        self.__add_samples(filtered_objects)
        self.__target_coordinates = target

        if self.__should_send_data():
            sample_request_model = self.__build_sample_request_model()

            self.__logger.debug(
                f'Sampled data (Trunk:{self.__trunk_sample_count}, Hood:{self.__hood_sample_count}): {sample_request_model} ')
            self.__controller_notifier.notify(sample_request_model.as_big_endian_bytes())
            self.__reset_samples()

    def __add_samples(self, filtered_objects: List[Object]) -> None:
        for obj in filtered_objects:
            if obj:
                sample = Sample.create(obj)
                self.__samples.append(sample)
                self.__increment_sample_count(sample.vehicle_part)

    def __increment_sample_count(self, part: VehiclePart) -> None:
        if part == VehiclePart.trunk:
            self.__trunk_sample_count += 1
        else:
            self.__hood_sample_count += 1

    def __reset_samples(self) -> None:
        self.__trunk_sample_count = 0
        self.__hood_sample_count = 0
        self.__samples.clear()

    def __should_send_data(self) -> bool:
        return self.__trunk_sample_count >= self.__sample_count and self.__hood_sample_count >= self.__sample_count

    def __build_sample_request_model(self) -> KinematicValues:
        trunk = self.__get_average_sample_values(VehiclePart.trunk)
        hood = self.__get_average_sample_values(VehiclePart.hood)

        kinematic_values = self.__kinematic_model.get_kinematic_values(tuple(trunk), tuple(hood),
                                                                       self.__target_coordinates)

        return kinematic_values

    def __get_average_sample_values(self, part_type: VehiclePart) -> Sample:
        positions = list(filter(lambda s: s.vehicle_part == part_type, self.__samples))
        x = y = 0
        n = len(positions)
        for pos in positions:
            x = x + pos.x
            y = y + pos.y

        return Sample(part_type, x // n, y // n)

    def dispose(self):
        self.__controller_notifier.dispose()
