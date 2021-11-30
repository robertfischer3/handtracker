from constants import scales

class Menu():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_sub_item(self, scale_name, img):
        pass

    def draw(self, img):
        for scale_name in scales.keys():
            self.draw_sub_item(scale_name, img)