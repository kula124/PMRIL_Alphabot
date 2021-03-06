import configparser

from cv2.cv2 import waitKey

from detector.VideoStream import VideoStream
from state.app_state_manager import AppStateManager
from utils import logger_factory


def main(config: configparser.ConfigParser):
    logger = logger_factory.get_logger()

    try:
        logger.info('Initializing image processor.')
        refresh_delay = config.getint('frame', 'refresh_delay')
        with VideoStream(config) as video_stream:
            with AppStateManager(config) as app_state_manager:
                logger.info('Successfully initialized image processor.')
                while True:
                    camera_feed_matrix = video_stream.read()
                    if camera_feed_matrix and len(camera_feed_matrix) > 0:
                        app_state_manager.get_state_action(camera_feed_matrix)()

                    waitKey(refresh_delay)
    except Exception as e:
        logger.error(f'Unhandled exception occurred. Shutting down! Reason:{e}')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    logger_factory.initialize(config)

    main(config)
