import configparser
import json
from typing import List, Tuple

from communication.controller_notifier import ControllerNotifier
from models.object import Object
from models.sample import Sample
from models.sample_request_model import SampleRequestModel
from models.vehicle_enum import VehiclePart


class CommunicationManager:
    def __init__(self, config: configparser.ConfigParser):
        self.__config = config
        self.__sample_count = int(self.__config['communication']['sample_count'])
        self.__current_sample_count = 0
        self.__samples: List[Sample] = []
        self.__target_coordinates = None
        self.__controller_notifier = ControllerNotifier(config)

    def handle(self, filtered_objects: List[Object], target: Tuple[int, int]) -> None:
        self.__add_samples(filtered_objects)
        self.__target_coordinates = target

        if self.__should_send_data():
            sample_request_model = self.__build_sample_request_model()

            request_json = json.dumps(sample_request_model.__dict__)
            self.__controller_notifier.notify(request_json)

    def __add_samples(self, filtered_objects: List[Object]) -> None:
        for obj in filtered_objects:
            self.__samples.append(Sample.create(obj))

    def __should_send_data(self) -> bool:
        return self.__current_sample_count >= self.__sample_count

    def __build_sample_request_model(self) -> SampleRequestModel:
        trunk = self.__get_average_sample_values(VehiclePart.trunk)
        hood = self.__get_average_sample_values(VehiclePart.hood)

        return SampleRequestModel.create(trunk, hood, self.__target_coordinates)

    def __get_average_sample_values(self, part_type: VehiclePart) -> Sample:
        positions = list(filter(lambda s: s.vehicle_part == part_type, self.__samples))
        x = y = 0
        n = len(positions)
        for pos in positions:
            x = x + pos.x
            y = y + pos.y

        return Sample(part_type, x // n, y // n)
