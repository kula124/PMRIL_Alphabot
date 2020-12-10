from models.object import Object
from models.vehicle_enum import VehiclePart


class Sample:
    def __init__(self, vehicle_part: VehiclePart, x: int, y: int):
        self.vehicle_part = vehicle_part
        self.x = x
        self.y = y

    @staticmethod
    def create(obj: Object) -> 'Sample':
        return Sample(VehiclePart[obj.get_label()], obj.get_x_pos(), obj.get_y_pos())

    def __iter__(self):
        yield self.x
        yield self.y
