from cv2.cv2 import findContours, RETR_CCOMP, CHAIN_APPROX_SIMPLE, putText, moments, inRange, MORPH_RECT, \
    getStructuringElement, erode, dilate

from models.object import Object
from presentation.drawer import Drawer


class Tracker:
    def __init__(self, config):
        self.__config = config
        self.__drawer = Drawer(config)

    def track_objects(self, filters, camera_feed_matrix, hsv_matrix):
        for filter in filters:
            threshold_matrix = inRange(hsv_matrix, (filter.H_MIN, filter.S_MIN, filter.V_MIN),
                                       (filter.H_MAX, filter.S_MAX, filter.V_MAX))
            enhanced_threshold_matrix = self.__morph_ops(threshold_matrix)

            self.__track_object(enhanced_threshold_matrix, camera_feed_matrix, "Item")

    def __morph_ops(self, threshold_matrix):
        # create structuring element that will be used to "dilate" and "erode" image.
        # the element chosen here is a 3px by 3px rectangle

        erode_element = getStructuringElement(MORPH_RECT, (3, 3))
        # dilate with larger element so make sure object is nicely visible
        dilate_element = getStructuringElement(MORPH_RECT, (8, 8))

        threshold_matrix = erode(threshold_matrix, erode_element, iterations=2)

        threshold_matrix = dilate(threshold_matrix, dilate_element, iterations=2)

        return threshold_matrix

    def __track_object(self, threshold_matrix, camera_feed_matrix, label) -> None:
        objects = []

        contours, hierarchy = findContours(threshold_matrix, RETR_CCOMP, CHAIN_APPROX_SIMPLE)

        if hierarchy is not None and hierarchy.size > int(self.__config['object']['MAX_NUM_OBJECTS']):
            putText(camera_feed_matrix, 'Too much noise! Adjust filter', (0, 50), 1, 2, (0, 0, 255), 2)
            return

        if hierarchy is not None and hierarchy.size > 0:
            i = 0
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

                i = hierarchy[0][i][0]

            if objects:
                self.__drawer.mark_objects(objects, camera_feed_matrix, contours, hierarchy)
