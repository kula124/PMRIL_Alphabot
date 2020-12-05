import configparser

from cv2.cv2 import waitKey

from app_state_manager import AppStateManager
from detector.video_provider import get_video_provider
from utils import logger_factory


def main(config: configparser.ConfigParser):
    logger = logger_factory.get_logger()

    logger.info('Initializing image processor.')
    video = get_video_provider(config)
    refresh_delay = config.getint('frame', 'refresh_delay')

    with AppStateManager(config) as app_state_manager:
        logger.info('Successfully initialized image processor.')
        while True:
            has_data, camera_feed_matrix = video.read()

            if not has_data:
                logger.error('No data from the source')
                return -1

            app_state_manager.get_state_action(camera_feed_matrix)()

            waitKey(refresh_delay)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    logger_factory.initialize(config)

    main(config)
