# import the necessary packages
import configparser

from detector.WebcamVideoStream import WebcamVideoStream


class VideoStream:
    def __init__(self, config: configparser.ConfigParser):
        if config.getboolean('frame', 'use_pi_camera'):
            from detector.PiVideoStream import PiVideoStream
            # initialize the picamera stream and allow the camera
            # sensor to warmup
            self.stream = PiVideoStream(config)

        else:
            self.stream = WebcamVideoStream(config)

    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()

    def read(self):
        return self.stream.read()

    def stop(self):
        self.stream.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self):
        self.stop()
