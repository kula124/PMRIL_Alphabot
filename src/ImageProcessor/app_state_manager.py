import configparser
from typing import Callable

from cv2.cv2 import cvtColor, COLOR_BGR2HSV

from communication.communication_manager import CommunicationManager
from detector.automatic_filter_tuner import AutomaticFilterTuner
from detector.target_provider import TargetProvider
from detector.tracker import Tracker
from presentation.presentation_manager import PresentationManager
from utils import logger_factory
from utils.filter_error import FilterError

FILTER_TUNED = 'FILTER_TUNED'
FILTER_UNTUNED = 'FILTER_UNTUNED'
TARGET_SELECTED = 'TARGET_SELECTED'
TARGET_UNSELECTED = 'TARGET_UNSELECTED'

"""
 Redux inspired app state manager
 Could be split up into action reducer store combination but
 for the sake of simplicity it's all in the same file
 as it's unlikely that the state will grow beyond this point
"""


class AppState:
    def __init__(self, is_filter_tuned: bool = False, is_target_selected: bool = False):
        self.is_filter_tuned = is_filter_tuned
        self.is_target_selected = is_target_selected

    def filter_tuned(self, tuned: bool):
        return AppState(tuned, self.is_target_selected)

    def target_selected(self, selected: bool):
        return AppState(self.is_filter_tuned, selected)


class AppStateManager:
    def __init__(self, config: configparser.ConfigParser):
        self.__logger = logger_factory.get_logger()
        self.__filter_tuner = AutomaticFilterTuner(self)
        self.__tracker = Tracker(config)
        self.__target_provider = TargetProvider(self)
        self.__communication_manager = CommunicationManager(config)
        self.__presentation_manager = PresentationManager(config, self.__filter_tuner.clickAndDrag_Rectangle,
                                                          self.__target_provider.target_selector)

        self.__state = AppState()

    def dispatch_action(self, action_type: str) -> None:
        if action_type == FILTER_TUNED:
            self.__state = self.__state.filter_tuned(True)
        if action_type == FILTER_UNTUNED:
            self.__state = self.__state.filter_tuned(False)
        if action_type == TARGET_SELECTED:
            self.__state = self.__state.is_target_selected(True)
        if action_type == TARGET_UNSELECTED:
            self.__state = self.__state.is_target_selected(False)

    def get_state_action(self, camera_feed_matrix) -> Callable:
        hsv_matrix = cvtColor(camera_feed_matrix, COLOR_BGR2HSV)
        self.__filter_tuner.record_hsv_values(camera_feed_matrix, hsv_matrix)

        if not self.__state.is_filter_tuned:
            return lambda: self.__presentation_manager.display_message(camera_feed_matrix,
                                                                       self.__filter_tuner.get_tuning_message())

        if not self.__state.is_target_selected:
            return lambda: self.__presentation_manager.display_message(camera_feed_matrix,
                                                                       self.__target_provider.get_target_selection_message())

        return lambda: self.__main_state_action(camera_feed_matrix, hsv_matrix)

    def __main_state_action(self, camera_feed_matrix, hsv_matrix) -> None:
        try:
            filtering_artifacts = self.__tracker.get_filtered_objects(self.__filter_tuner.recorded_hsv_filters,
                                                                      hsv_matrix)

            self.__presentation_manager.refresh(camera_feed_matrix, filtering_artifacts)

            flat_object_list = [obj for sublist in [art[0] for art in filtering_artifacts] for obj in sublist]

            self.__communication_manager.handle(flat_object_list, self.__target_provider.target)
        except FilterError as e:
            self.__presentation_manager.display_error(camera_feed_matrix, e.message)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__communication_manager.dispose()
