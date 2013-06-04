# Encoding: UTF-8

from utils import GameObject


class Button(GameObject):

    def __init__(self, position, image, size):
        GameObject.__init__(self, image, position)
        self.size = size
        self.width = size[0]
        self.height = size[1]

    def inside_x(self, x):
        return x >= self.position[0] and x <= self.position[0] + self.width

    def inside_y(self, y):
        return y >= self.position[1] and y <= self.position[1] + self.height

    def check_click(self, position):
        x, y = position
        return self.inside_x(x) and self.inside_y(y)

    def click(self):
        pass
