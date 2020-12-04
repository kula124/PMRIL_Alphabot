from typing import List, Tuple

from models.sample import Sample


class SampleRequestModel:
    def __init__(self, robot: List[int], target: List[int]):
        if len(robot) != 4:
            raise ValueError('robot list must contain 4 coordinates')
        if len(target) != 2:
            raise ValueError('target list must contain 2 coordinates')

        self.robot: List[int] = robot
        self.target: List[int] = target

    @staticmethod
    def create(trunk_sample: Sample, hood_sample: Sample, target: Tuple[int, int]) -> 'SampleRequestModel':
        robot = [trunk_sample.x, trunk_sample.y, hood_sample.x, hood_sample.y]
        target = [target[0], target[1]]

        return SampleRequestModel(robot, target)
