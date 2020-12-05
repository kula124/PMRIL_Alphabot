from typing import Tuple

from cv2.cv2 import EVENT_MBUTTONUP, EVENT_FLAG_ALTKEY

from app_state_manager import AppStateManager, TARGET_UNSELECTED, TARGET_SELECTED


class TargetProvider:
    def __init__(self, app_state_manager: AppStateManager):
        self.__app_state_manager = app_state_manager
        self.target: Tuple[int, int] = None

    # noinspection PyUnusedLocal
    # Needs to be there for the signature
    def target_selector(self, event: int, x: int, y: int, flags: int, video_feed) -> None:
        if event == EVENT_MBUTTONUP:
            if flags == EVENT_FLAG_ALTKEY:
                self.target = None
                self.__app_state_manager.dispatch_action(TARGET_UNSELECTED)
            else:
                self.target = (x, y)
                self.__app_state_manager.dispatch_action(TARGET_SELECTED)

    @staticmethod
    def get_target_selection_message() -> str:
        return 'Select the target'
