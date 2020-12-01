from cv2.cv2 import EVENT_LBUTTONDOWN, EVENT_MOUSEMOVE, EVENT_LBUTTONUP, EVENT_RBUTTONDOWN, rectangle

from models.hsv_filter import HSVFilter


class AutomaticFilterTuner:
    def __init__(self, on_reset_filter=lambda: None):
        self.__is_mouse_dragging = False
        self.__initial_click_point = None
        self.__current_mouse_point = None
        self.__mouse_move = False
        self.__rectangle_roi = None
        self.__rectangle_selected = False
        self.__on_reset_filter = on_reset_filter
        self.recorded_hsv_filters = []

    def clickAndDrag_Rectangle(self, event, x, y):
        if event == EVENT_LBUTTONDOWN and not self.__is_mouse_dragging:
            # keep track of initial point clicked
            self.__initial_click_point = (x, y)
            # user has begun dragging the mouse
            self.__is_mouse_dragging = True

        # * user is dragging the mouse */
        if event == EVENT_MOUSEMOVE and self.__is_mouse_dragging:
            # keep track of current mouse point
            self.__current_mouse_point = (x, y)
            # user has moved the mouse while clicking and dragging
            self.__mouse_move = True

        # user has released left button
        if event == EVENT_LBUTTONUP and self.__is_mouse_dragging:
            # set rectangle ROI to the rectangle that the user has selected
            self.__rectangle_roi = (self.__initial_click_point, self.__current_mouse_point);

            # reset boolean variables
            self.__is_mouse_dragging = False
            self.__mouse_move = False
            self.__rectangle_selected = True

        if event == EVENT_RBUTTONDOWN:
            self.__rectangle_selected = False
            self.recorded_hsv_filters.clear()
            self.__on_reset_filter()

    def record_hsv_values(self, frame, hsv_frame):
        if self.__mouse_move:
            # draw the click
            rectangle(frame, self.__initial_click_point, self.__current_mouse_point, (0, 255, 0))
            return
        if not self.__rectangle_selected:
            return

        h_min = s_min = v_min = 255
        h_max = s_max = v_max = 0

        for i in range(self.__rectangle_roi[0][0], self.__rectangle_roi[1][0]):
            for j in range(self.__rectangle_roi[0][1], self.__rectangle_roi[1][1]):
                hsv_px = hsv_frame[(j, i)]

                h_min = min(h_min, hsv_px[0])
                h_max = max(h_max, hsv_px[0])
                s_min = min(s_min, hsv_px[1])
                s_max = max(s_max, hsv_px[1])
                v_min = min(v_min, hsv_px[2])
                v_max = max(v_max, hsv_px[2])

        self.__rectangle_selected = False

        self.recorded_hsv_filters.append(HSVFilter(h_min, h_max, s_min, s_max, v_min, v_max))