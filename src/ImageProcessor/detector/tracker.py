from typing import Tuple, List

from cv2.cv2 import findContours, RETR_CCOMP, CHAIN_APPROX_SIMPLE, moments
from numpy import ndarray

from models.object import Object
from utils import logger_factory
from utils.filter_error import FilterError
from utils.graphic import perform_morphological_operations, get_threshold_matrix


class Tracker:
    def __init__(self, config):
        self.__config = config
        self.__logger = logger_factory.get_logger()

    def get_filtered_objects(self, filters, hsv_matrix) -> List[Tuple[List[Object], List[ndarray], ndarray]]:
        filtered_objects = []

        for filter in filters:
            threshold_matrix = get_threshold_matrix(hsv_matrix, filter)
            enhanced_threshold_matrix = perform_morphological_operations(threshold_matrix)

            filtered_objects.append(self.__get_object(enhanced_threshold_matrix, filter.label))

        return filtered_objects

    def __get_object(self, threshold_matrix, label) -> Tuple[List[Object], List[ndarray], ndarray]:
        objects = []

        contours, hierarchy = findContours(threshold_matrix, RETR_CCOMP, CHAIN_APPROX_SIMPLE)

        if hierarchy is not None and hierarchy.size > int(self.__config['object']['MAX_NUM_OBJECTS']):
            self.__logger.error(f'Number of {label} objects detected ({hierarchy.size}) exceeded max number.')
            raise FilterError('Too much noise! Adjust filter')

        if hierarchy is not None and hierarchy.size > 0:
            i = 0
            self.__logger.debug(f'Found {hierarchy.size} {label}.')
            while i >= 0:
                moment = moments(contours[i])

                area = moment['m00']
                # if the area is less than 20 px by 20px then it is probably just noise
                # if the area is the same as the 3 / 2 of the image size, probably just a bad filter
                # we only want the object with the largest area so we safe a reference area each
                # iteration and compare it to the area in the next iteration.

                if area > int(self.__config['object']['MIN_OBJECT_AREA']):
                    obj = Object(label=label, x=moment['m10'] / area, y=moment['m01'] / area)
                    objects.append(obj)
                else:
                    self.__logger.debug(f'Object with area f{area} is too small.')

                i = hierarchy[0][i][0]

            return objects, contours, hierarchy

        return [], None, None
