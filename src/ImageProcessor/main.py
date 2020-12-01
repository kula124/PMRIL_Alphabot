import configparser

from cv2.cv2 import waitKey, cvtColor, COLOR_BGR2HSV

from detector.automatic_filter_tuner import AutomaticFilterTuner
from detector.video_provider import get_video_provider
from presentation.presentation_manager import PresentationManager


def main(config: configparser.ConfigParser):
    filter_tuner = AutomaticFilterTuner()
    presentation_manager = PresentationManager(config)
    video = get_video_provider(config)

    waitKey(1000)

    while True:
        has_data, camera_feed_matrix = video.read()

        if not has_data:
            print('No data from the source')
            return -1

        hsv_matrix = cvtColor(camera_feed_matrix, COLOR_BGR2HSV)

        filter_tuner.record_hsv_values(camera_feed_matrix, hsv_matrix)

        presentation_manager.refresh(camera_feed_matrix, hsv_matrix)

        waitKey(30)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    main(config)
