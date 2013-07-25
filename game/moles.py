# Encoding: UTF-8

from utils import GameObject


class Mole(GameObject):

    coordenates = (0, 0)
    alive = True
    alive_timer = 50
    killed = False
    points = 1

    def __init__(self, position, coordenates, image='mole.png'):
        GameObject.__init__(self, image, position)
        self.coordenates = coordenates

    def update(self, dt):
        self.alive_timer -= 1

        if not self.alive_timer:
            self.alive = False


class FemaleMole(Mole):

    def __init__(self, position, coordenates, image='female_mole.png'):
        Mole.__init__(self, position, coordenates, image)
