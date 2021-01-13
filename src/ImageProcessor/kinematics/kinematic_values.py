import struct


class KinematicValues:
    def __init__(self, v: float, w: float):
        self.v = v
        self.w = w

    def as_big_endian_bytes(self) -> bytearray:
        """
        First 4 bytes are v and last 4 are w
        :return: byte array representing speed and angular speed
        """
        return bytearray(struct.pack('!f', self.v)) + bytearray(struct.pack('!f', self.w))

    def __repr__(self):
        return f'v:{self.v}, w:{self.w}'
