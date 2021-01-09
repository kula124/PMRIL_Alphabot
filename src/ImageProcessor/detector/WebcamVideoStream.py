import configparser
from threading import Thread

from cv2 import CAP_PROP_FRAME_WIDTH, VideoCapture, CAP_PROP_FRAME_HEIGHT


class WebcamVideoStream:
    def __init__(self, config: configparser.ConfigParser):
        self.stream = VideoCapture(config.getint('frame', 'input_slot'))
        self.stream.set(CAP_PROP_FRAME_WIDTH, int(config['frame']['width']))
        self.stream.set(CAP_PROP_FRAME_HEIGHT, int(config['frame']['height']))

        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        """
        Start the thread to read frames from the video stream
        :return:
        """
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Infinite loop until th thread is stopped
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
