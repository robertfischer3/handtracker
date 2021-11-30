from constants import scales
import cv2

class Menu():

    def __init__(self, x, y, menu_dictionary, alpha=0.7, btm_text_color=(0, 255, 0), visible=True):
        self.x = x
        self.y = y
        self.alpha = alpha  # Transparency factor.
        self.btm_text_color = btm_text_color
        self.column_number = 2
        self.row_number = 8
        self.visible = visible
        self.menu_dictionary = menu_dictionary

    def set_column_number(self, column_number=2):
        self.column_number = column_number

    def set_row_number(self, row_number):
        # Sets the maximum row count for the menu item
        self.row_number = row_number

    def set_visible(self, visible=True):
        # Sets the controls to make visible or not
        self.visible = visible

    def draw_sub_item(self, scale_name, overlay_img, x, y):

        cv2.putText(overlay_img, scale_name, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, self.btm_text_color, 2, cv2.LINE_AA)
        return overlay_img

    def draw(self, img):

        # Create an overlay image to place buttons on
        overlay = img.copy()

        current_y = self.y
        current_x = self.x

        current_row = 0
        for scale_name in self.menu_dictionary.keys():
            if self.column_number > 1 and current_row >= self.row_number:
                current_x += 250
                current_row = 0
                current_y = self.y

            overlay = self.draw_sub_item(scale_name, overlay, current_x, current_y)
            current_y += 70
            current_row += 1

        image_new = cv2.addWeighted(overlay, self.alpha, img, 1 - self.alpha, 0)

        return image_new