# Encoding: UTF-8

from utils import GameObject


class Mole(GameObject):

    coordenates = (0, 0)
    alive_timer = 50
    dead_time = 5
    killed = False
    escaped = False
    points = 1
    lives = 1

    def __init__(self, position, coordenates, image_set=['mole.png', 'mole_dead.png']):
        GameObject.__init__(self, image_set, position)
        self.coordenates = coordenates

    def update(self, dt):
        self.alive_timer -= 1

        if not self.alive_timer:
            self.escaped = True

    def loose_life(self):
        self.lives -= 1

    def die(self):
        self.frame = -1
        self.dead_time -= 1
        if not self.dead_time:
            return True


class FemaleMole(Mole):

    def __init__(self, position, coordenates,
                    image_set=['female_mole.png', 'female_mole_dead.png']):
        Mole.__init__(self, position, coordenates, image_set)


class SpeedMole(Mole):
    alive_timer = 25
    points = 2

    def __init__(self, position, coordenates,
                    image_set=['mole_speed.png', 'mole_dead.png']):
        Mole.__init__(self, position, coordenates, image_set)


class CapMole(Mole):
    lives = 2
    points = 2

    def loose_life(self):
        if self.lives == CapMole.lives:
            self.frame = 1
        return super(CapMole, self).loose_life()

    def __init__(self, position, coordenates,
            image_set=['mole_cap.png', 'mole_cap_confused.png', 'mole_dead.png']):
        Mole.__init__(self, position, coordenates, image_set)
