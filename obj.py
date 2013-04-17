# Encoding: UTF-8

import os
import sys
import getopt

import pygame

from random import randint

try:
    import android
except ImportError:
    android = None

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


class Sign(GameObject):

    def __init__(self, position, image, score):
        GameObject.__init__(self, image, position)
        self.font = pygame.font.Font('FreeSans.ttf', 20)
        self.label_position = (position[0] + 15, position[1] + 30)
        self.score = score

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.label, self.label_position)

    def update(self, dt):
        self.label = self.font.render('Points: %s' % self.score, False, (100, 50, 0))


class Hole(GameObject):

    coordenates = (0, 0)
    active = False
    mole = None
    refresh_counter = 24

    def __init__(self, position, image, coordenates):
        GameObject.__init__(self, image, position)
        self.coordenates = coordenates

    def update(self, dt):
        if self.active:
            self.refresh_counter -= 1


class Mole(GameObject):

    coordenates = (0, 0)
    alive = True
    alive_timer = 60
    killed = False

    def __init__(self, position, image, coordenates):
        GameObject.__init__(self, image, position)
        self.coordenates = coordenates

    def update(self, dt):
        self.alive_timer -= 1

        if not self.alive_timer:
            self.alive = False


class Player:

    lifes = 5
    score = 0


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

    player = Player()

    level_map = [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]

    def __init__(self, size):
        pygame.init()
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        self.screen = pygame.display.set_mode(size)
        self.screen_size = self.screen.get_size()
        # pygame.mouse.set_visible(0)
        pygame.display.set_caption('Mole Hole')
        self.score_sign = Sign((200, 100), 'sign.png', self.player.score)

    def click_event(self):
        x, y = pygame.mouse.get_pos()

        x = (x - self.top_margin) / self.hole_width
        y = (y - self.left_margin) / self.hole_height

        for mole in self.actors_dict['moles']:
            if mole.coordenates == (y, x):
                self.kill_mole(mole, True)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_event()

    def actors_update(self, dt):
        self.background.update(dt)

        for actor in self.actors_dict.values():
            actor.update(dt)

        self.score_sign.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        for actor in self.actors_dict.values():
            actor.draw(self.screen)

        self.score_sign.draw(self.screen)

    def refresh_holes(self):
        for hole in self.active_holes:
            if not hole.refresh_counter:
                self.unactive_holes.append(hole)
                self.active_holes.remove(hole)
                hole.active = False
                hole.refresh_counter = 24

    def kill_mole(self, mole, killed=False):
        if killed:
            self.player.score += 1
        else:
            self.player.lifes -= 1

        print self.player.lifes
        print self.player.score

        self.active_holes.append(mole.hole)
        mole.hole.active = True
        mole.kill()

    def refresh_moles(self):
        for mole in self.actors_dict['moles']:
            if not mole.alive:
                self.kill_mole(mole)

    def manage(self):
        self.create_moles()
        self.refresh_moles()
        self.refresh_holes()
        self.refresh_player()

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

        if not randint(0, self.difficulty):
            if self.unactive_holes:
                hole_index = randint(0, len(self.unactive_holes) - 1)
                hole = self.unactive_holes[hole_index]

                mole = Mole(hole.position, "mole1.png", hole.coordenates)
                self.actors_dict['moles'].add(mole)
                mole.hole = hole
                self.unactive_holes.remove(hole)

    def refresh_player(self):
        if self.player.lifes <= 0:
            print 'FODEU!!!'

    def loop(self):
        self.background = Background("background.png")
        clock = pygame.time.Clock()
        dt = 50
        self.interval = 1
        self.difficulty = 100 / 5
        self.unactive_holes = []
        self.active_holes = []
        self.actors_dict = {
            "holes": pygame.sprite.RenderPlain(),
            "moles": pygame.sprite.RenderPlain(),
            }

        self.generate_holes()

        while self.run:
            clock.tick(1200 / 50)
            self.interval += 1

            self.score_sign.score = self.player.score
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
