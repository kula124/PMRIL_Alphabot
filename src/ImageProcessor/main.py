import configparser

from cv2.cv2 import waitKey

from detector.VideoStream import VideoStream
from state.app_state_manager import AppStateManager
from utils import logger_factory


def main(config: configparser.ConfigParser):
    logger = logger_factory.get_logger()

    logger.info('Initializing image processor.')
    refresh_delay = config.getint('frame', 'refresh_delay')
    with VideoStream(config).start() as video_stream:
        with AppStateManager(config) as app_state_manager:
            logger.info('Successfully initialized image processor.')
            while True:
                camera_feed_matrix = video_stream.read()

                app_state_manager.get_state_action(camera_feed_matrix)()

                waitKey(refresh_delay)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    logger_factory.initialize(config)

    main(config)
