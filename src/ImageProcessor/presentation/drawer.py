from typing import List, Tuple

from cv2.cv2 import circle, putText, drawContours, drawMarker, MARKER_TILTED_CROSS

from models.object import Object


class Drawer:
    def __init__(self, config):
        self.__draw_contours = config.getboolean('drawer', 'draw_contours')
        self.__center_marker_radius = config.getint('drawer', 'center_marker_radius')

    def mark_objects(self, objects: List[Object], frame, contours, hierarchy) -> None:
        for i, obj in enumerate(objects):
            contour_position = (int(obj.get_x_pos()), int(obj.get_y_pos()))
            pos_text_position = (int(obj.get_x_pos()), int(obj.get_y_pos() + 20))
            color_text_position = (int(obj.get_x_pos()), int(obj.get_y_pos() - 30))

            circle(frame, contour_position, self.__center_marker_radius, obj.get_color())
            putText(frame, f'{contour_position[0]}, {contour_position[1]}', pos_text_position, 1, 1, obj.get_color())
            putText(frame, obj.get_label(), color_text_position, 1, 2, obj.get_color())

            if self.__draw_contours:
                drawContours(frame, contours, i, obj.get_color(), 1, 8, hierarchy)

    def mark_target(self, target: Tuple[int, int], frame) -> None:
        drawMarker(frame, target, (0, 0, 255), MARKER_TILTED_CROSS, thickness=2)
