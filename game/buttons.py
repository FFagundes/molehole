# Encoding: UTF-8

from utils import GameObject


class Button(GameObject):

    def __init__(self, position, image, name):
        GameObject.__init__(self, image, position)
        self.name = name

    def _inside_x(self, x):
        return x >= self.position[0] and x <= self.position[0] + self.rect.width

    def _inside_y(self, y):
        return y >= self.position[1] and y <= self.position[1] + self.rect.height

    def check_click(self, position):
        x, y = position
        return self._inside_x(x) and self._inside_y(y)

    def click(self):
        pass


class StartButton(Button):

    def __init__(self, position=(65, 140), name='start', image='btn_start.png'):
        Button.__init__(self, position, image, name)


class CreditsButton(Button):

    def __init__(self, position=(0, 0), name='credits', image='btn_credits.png'):
        Button.__init__(self, position, image, name)


class BackButton(Button):

    def __init__(self, position=(300, 270), name='back', image='btn_credits.png'):
        Button.__init__(self, position, image, name)
