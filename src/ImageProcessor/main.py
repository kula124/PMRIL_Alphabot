import configparser

from cv2.cv2 import waitKey, cvtColor, COLOR_BGR2HSV

from detector.automatic_filter_tuner import AutomaticFilterTuner
from detector.tracker import Tracker
from detector.video_provider import get_video_provider
from presentation.presentation_manager import PresentationManager
from utils.filter_error import FilterError


def main(config: configparser.ConfigParser):
    filter_tuner = AutomaticFilterTuner()
    tracker = Tracker(config)
    presentation_manager = PresentationManager(config, filter_tuner)

    video = get_video_provider(config)

    waitKey(1000)

    while True:
        has_data, camera_feed_matrix = video.read()

        if not has_data:
            print('No data from the source')
            return -1

        hsv_matrix = cvtColor(camera_feed_matrix, COLOR_BGR2HSV)

        filter_tuner.record_hsv_values(camera_feed_matrix, hsv_matrix)

        if filter_tuner.is_tuned():
            try:
                filtered_objects = tracker.get_filtered_objects(filter_tuner.recorded_hsv_filters, hsv_matrix)

                presentation_manager.refresh(camera_feed_matrix, filtered_objects)
            except FilterError as e:
                presentation_manager.display_error(camera_feed_matrix, e.message)
        else:
            presentation_manager.display_message(camera_feed_matrix, filter_tuner.get_tuning_message())

        waitKey(config['frame']['refresh_delay'])


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    main(config)
