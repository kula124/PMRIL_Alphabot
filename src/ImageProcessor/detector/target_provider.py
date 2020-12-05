from typing import Tuple

from cv2.cv2 import EVENT_MBUTTONUP, EVENT_FLAG_ALTKEY


class TargetProvider:
    def __init__(self):
        self.target: Tuple[int, int] = None

    # noinspection PyUnusedLocal
    # Needs to be there for the signature
    def target_selector(self, event: int, x: int, y: int, flags: int, video_feed) -> None:
        if event == EVENT_MBUTTONUP:
            if flags == EVENT_FLAG_ALTKEY:
                self.target = None
            else:
                self.target = (x, y)

    def is_target_selected(self) -> bool:
        return self.target is not None

    @staticmethod
    def get_target_selection_message() -> str:
        return 'Select the target'
