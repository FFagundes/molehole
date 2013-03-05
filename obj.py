# Encoding: UTF-8

import os
import sys
import getopt

import pygame

from random import randint

images_dir = os.path.join("images")


class Background:

    image = None

    def __init__(self, image):
        if isinstance(image, str):
            image = os.path.join(images_dir, image)
            image = pygame.image.load(image).convert()

        self.isize = image.get_size()
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()
        back = pygame.Surface(screen_size)
        back.blit(image, (0, 0))
        self.image = back

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class GameObject(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        if isinstance(self.image, str):
            self.image = os.path.join(images_dir, self.image)
            self.image = pygame.image.load(self.image)

        self.position = position
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.set_pos(position)

    def update(self, dt):
        pass
        # aqui é onde devo matar as topeiras

    def set_pos(self, pos):
        self.rect.topleft = (pos[0], pos[1])


class Hole(GameObject):

    coordenates = (0, 0)
    active = False

    def __init__(self, position, image, coordenates):
        GameObject.__init__(self, image, position)
        self.coordenates = coordenates


class Mole(GameObject):

    alive = True
    alive_timer = 60
    killed = False

    def __init__(self, position, image):
        GameObject.__init__(self, image, position)


class Game:

    #constantes
    screen = None
    screen_size = None
    run = True
    actors_dict = None
    background = None

    hole_width = 128
    hole_height = 96

    top_margin = 80
    left_margin = 260

    level_map = [
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1],
                ]

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Mole Hole')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def actors_update(self, dt):
        self.background.update(dt)

        for actor in self.actors_dict.values():
            actor.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        for actor in self.actors_dict.values():
            actor.draw(self.screen)

    def manage(self):
        self.create_moles()

    def generate_holes(self):
        for (x, lin) in enumerate(self.level_map):
            for (y, col) in enumerate(lin):
                if col:

                    ver_align = (y * self.hole_width) + self.top_margin
                    hor_align = (x * self.hole_height) + self.left_margin

                    hole = Hole((ver_align, hor_align), "hole1.png", (x, y))

                    self.actors_dict['holes'].add(hole)
                    self.unactive_holes.append(hole)

    def create_moles(self):

        if(randint(0, self.difficulty) == 0):

            if self.unactive_holes:
                hole_index = randint(0, len(self.unactive_holes) - 1)
                hole = self.unactive_holes[hole_index]

                mole = Mole(hole.position, "mole1.png")
                self.actors_dict['moles'].add(mole)
                self.unactive_holes.remove(hole)

    def loop(self):
        self.background = Background("background.png")
        clock = pygame.time.Clock()
        dt = 50
        self.interval = 1
        self.difficulty = 5
        self.unactive_holes = []
        self.actors_dict = {
            "holes": pygame.sprite.RenderPlain(),
            "moles": pygame.sprite.RenderPlain(),
            }

        self.generate_holes()

        while self.run:
            clock.tick(1000 / dt)
            self.interval += 1

            self.handle_events()
            self.actors_update(dt)
            self.manage()
            self.actors_draw()
            pygame.display.flip()

            # print "FPS: %0.2f" % clock.get_fps()


def main():
    game = Game((800, 600))
    game.loop()

if __name__ == '__main__':
    main()
