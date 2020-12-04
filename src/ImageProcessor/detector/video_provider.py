import configparser

from cv2 import CAP_PROP_FRAME_WIDTH, VideoCapture, CAP_PROP_FRAME_HEIGHT


def get_video_provider(config: configparser.ConfigParser):
    capture = VideoCapture()

    capture.open(int(config['frame']['input_slot']))
    capture.set(CAP_PROP_FRAME_WIDTH, int(config['frame']['width']))
    capture.set(CAP_PROP_FRAME_HEIGHT, int(config['frame']['height']))

    return capture
