# Encoding: UTF-8

from utils import GameObject


class Mole(GameObject):

    coordenates = (0, 0)
    alive = True
    alive_timer = 25
    killed = False

    def __init__(self, position, image, coordenates):
        GameObject.__init__(self, image, position)
        self.coordenates = coordenates

    def update(self, dt):
        self.alive_timer -= 1

        if not self.alive_timer:
            self.alive = False
