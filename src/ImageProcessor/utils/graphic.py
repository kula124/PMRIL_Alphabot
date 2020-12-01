from cv2.cv2 import getStructuringElement, MORPH_RECT, erode, dilate, inRange

from models.hsv_filter import HSVFilter


def perform_morphological_operations(threshold_matrix):
    # create structuring element that will be used to "dilate" and "erode" image.
    # the element chosen here is a 3px by 3px rectangle

    erode_element = getStructuringElement(MORPH_RECT, (3, 3))
    # dilate with larger element so make sure object is nicely visible
    dilate_element = getStructuringElement(MORPH_RECT, (8, 8))

    threshold_matrix = erode(threshold_matrix, erode_element, iterations=2)

    threshold_matrix = dilate(threshold_matrix, dilate_element, iterations=2)

    return threshold_matrix


def get_threshold_matrix(hsv_matrix, hsv_filter: HSVFilter):
    return inRange(hsv_matrix, (hsv_filter.H_MIN, hsv_filter.S_MIN, hsv_filter.V_MIN),
                   (hsv_filter.H_MAX, hsv_filter.S_MAX, hsv_filter.V_MAX))
