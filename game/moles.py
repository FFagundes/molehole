# Encoding: UTF-8

from utils import GameObject


class Mole(GameObject):

    coordenates = (0, 0)
    alive = True
    alive_timer = 50
    dead_time = 5
    killed = False
    points = 1
    lives = 1

    def __init__(self, position, coordenates, image_set=['mole.png', 'mole_dead.png']):
        GameObject.__init__(self, image_set, position)
        self.coordenates = coordenates

    def update(self, dt):
        self.alive_timer -= 1

        if not self.alive_timer:
            self.alive = False

        if not self.dead_time:
            self.kill()

    def die(self):
        self.dead_time -= 1
        if not self.dead_time:
            return False


class FemaleMole(Mole):

    def __init__(self, position, coordenates, image_set=['female_mole.png', 'female_mole_dead.png']):
        Mole.__init__(self, position, coordenates, image_set)


class SpeedMole(Mole):
    alive_timer = 25

    def __init__(self, position, coordenates, image_set='mole_speed.png'):
        Mole.__init__(self, position, coordenates, image_set)


class CapMole(Mole):
    lives = 2

    def __init__(self, position, coordenates, image_set='mole_cap.png'):
        Mole.__init__(self, position, coordenates, image_set)
