import configparser


class HSVFilter:
    def __init__(self, H_MIN, H_MAX, S_MIN, S_MAX, V_MIN, V_MAX, ):
        self.H_MIN = int(H_MIN)
        self.H_MAX = int(H_MAX)
        self.S_MIN = int(S_MIN)
        self.S_MAX = int(S_MAX)
        self.V_MIN = int(V_MIN)
        self.V_MAX = int(V_MAX)

    def set_H_MIN(self, val):
        self.H_MIN = val

    def set_H_MAX(self, val):
        self.H_MAX = val

    def set_S_MIN(self, val):
        self.S_MIN = val

    def set_S_MAX(self, val):
        self.S_MAX = val

    def set_V_MIN(self, val):
        self.V_MIN = val

    def set_V_MAX(self, val):
        self.V_MAX = val


def get_from_configuration(config: configparser.ConfigParser) -> HSVFilter:
    return HSVFilter(int(config['HSV_filter_values']['H_MIN']), int(config['HSV_filter_values']['H_MAX']),
                     int(config['HSV_filter_values']['S_MIN']), int(config['HSV_filter_values']['S_MAX']),
                     int(config['HSV_filter_values']['V_MIN']), int(config['HSV_filter_values']['V_MAX']))
