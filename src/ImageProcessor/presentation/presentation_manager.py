import configparser
from typing import List, Tuple, Callable

from cv2 import namedWindow, setMouseCallback, imshow
from cv2.cv2 import putText
from numpy import ndarray

from models.object import Object
from presentation.drawer import Drawer


class PresentationManager:
    def __init__(self, config: configparser.ConfigParser, *mouse_callbacks: Callable):
        self.__config = config
        self.__drawer = Drawer(config)
        self.__mouse_callbacks = mouse_callbacks

        self.__initialize()

    def refresh(self, camera_feed, filtered_objects: List[Tuple[List[Object], List[ndarray], ndarray]],
                target: Tuple[int, int]) -> None:
        """Redraws the image based on camera feed with any objects that might appear"""

        for (objects, contours, hierarchy) in filtered_objects:
            self.__drawer.mark_objects(objects, camera_feed, contours, hierarchy)

        self.__drawer.mark_target(target, camera_feed)

        self.__refresh(camera_feed)

    def display_error(self, camera_feed, message: str) -> None:
        putText(camera_feed, message, (0, 50), 1, 2, (255, 0, 0), 2)
        self.__refresh(camera_feed)

    def display_message(self, camera_feed, message: str) -> None:
        putText(camera_feed, message, (0, 50), 1, 2, (0, 0, 255), 2)
        self.__refresh(camera_feed)

    def register_mouse_callback(self, callback: Callable) -> None:
        self.__mouse_callbacks.append(callback)

    def __refresh(self, camera_feed):
        # TODO: Make this configurable
        # imshow(config['window']['name2'], compound_threshold_matrix if compound_threshold_matrix is not None else blank_image)
        # imshow(self.__config['window']['name1'], hsv_matrix)
        # imshow('morphed', morphed_matrix)

        imshow(self.__config['window']['original'], camera_feed)

        # imshow(config['window']['thresholded'], threshold_matrix)
        # imshow(config['window']['name1'], hsv_matrix)
        # imshow('morphed', morphed_matrix)

    def __initialize(self) -> None:
        namedWindow(self.__config['window']['original'])
        setMouseCallback(self.__config['window']['original'], self.__on_mouse_handler)

    def __on_mouse_handler(self, event, x, y, flags, video_feed):
        for callback in self.__mouse_callbacks:
            callback(event, x, y, flags, video_feed)
