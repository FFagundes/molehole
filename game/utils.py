# Encoding: UTF-8

import os
import pygame
from settings import images_dir


class Background(object):
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

    def __init__(self, score, position=(175, 33), image='sign.png'):
        GameObject.__init__(self, image, position)
        self.font = pygame.font.Font('FreeSans.ttf', 16)
        self.label_position = (position[0] + 10, position[1] + 13)
        self.score = score

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.label, self.label_position)

    def update(self, dt):
        self.label = self.font.render('Score: %s' %
                                self.score, False, (100, 50, 0))


class LivesSign(Sign):
    def __init__(self, score, position=(360, 20), image='sign.png'):
        Sign.__init__(self, score, position, image)

    def update(self, dt):
        self.label = self.font.render('Lifes: %s' %
                                self.score, False, (100, 50, 0))


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


class Player(object):

    lives = 5
    score = 0
