# Encoding: UTF-8

from utils import GameObject


class Button(GameObject):

    def __init__(self, position, image, name):
        GameObject.__init__(self, image, position)
        self.name = name

    def check_click(self, position):
        return self.rect.collidepoint(position)

    def click(self):
        pass


class StartButton(Button):

    def __init__(self, position=(65, 140), name='start', image='btn_start.png'):
        Button.__init__(self, position, image, name)


class CreditsButton(Button):

    def __init__(self, position=(0, 0), name='credits', image='btn_credits.png'):
        Button.__init__(self, position, image, name)


class BackButton(Button):

    def __init__(self, position=(385, 260), name='back', image='btn_back.png'):
        Button.__init__(self, position, image, name)


class PlayButton(Button):

    def __init__(self, position=(0, 222), name='play', image='btn_tuto_start.png'):
        Button.__init__(self, position, image, name)


class NextButton(Button):

    def __init__(self, position=(385, 260), name='next', image='btn_tuto_next.png'):
        Button.__init__(self, position, image, name)
