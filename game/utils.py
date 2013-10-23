# Encoding: UTF-8

import os
import pygame
from settings import images_dir, fonts_dir, sounds_dir
from random import randint

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


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


class HammerBlow(object):
    sounds = []

    def __init__(self):

        for x in range(4):
            sound_mixer = mixer.Sound(os.path.join(
                                sounds_dir, 'blow' + str(x + 1) + '.ogg'))
            self.sounds.append(sound_mixer)

    def play(self):
        blow = randint(0, len(self.sounds) - 1)
        self.sounds[blow].play()


class HighScore(object):

    def __init__(self, high_score, position=(10, 295), size=16):
        self.score = str(high_score)
        self.size = size
        self.position = position
        font_path = os.path.join(fonts_dir, 'FreeSans.ttf')
        self.font = pygame.font.Font(font_path, self.size)
        self.label = self.font.render(self.score, False, (200, 170, 50))

    def draw(self, screen):
        screen.blit(self.label, self.position)


class GameObject(pygame.sprite.Sprite):

    frame = 0

    def __init__(self, image_set, position):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(image_set, list):
            self.image_set = image_set
        else:
            self.image_set = [image_set]

        for counter, image in enumerate(self.image_set):
            if isinstance(image, str):
                image = os.path.join(images_dir, image)
                self.image_set[counter] = pygame.image.load(image)

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

    @property
    def image(self):
        return self.image_set[self.frame]


class LifeCorns(GameObject):

    corns = 5
    space = 32

    def __init__(self, image='corn.png', position=(5, 5)):
        self.initial_corns = self.corns
        self.dead_image = os.path.join(images_dir, 'dead_corn.png')
        self.dead_image = pygame.image.load(self.dead_image)

        GameObject.__init__(self, image, position)

    def draw(self, screen):
        x = 0
        for x in range(self.corns):
            screen.blit(self.image,
                    (self.position[0] + (self.space * x), self.position[1]))

        for y in range(self.initial_corns - self.corns):
            screen.blit(self.dead_image,
                    (self.position[0] + (self.space * self.corns)
                                            + (self.space * y), self.position[1]))


class Sign(GameObject):

    def __init__(self, score, position=(280, 22), image='sign.png'):
        GameObject.__init__(self, image, position)
        font_path = os.path.join(fonts_dir, 'FreeSans.ttf')
        self.font = pygame.font.Font(font_path, 16)
        self.label_position = (position[0] + 25, position[1] + 28)
        self.score = score
        self.color = (100, 50, 0)

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.label, self.label_position)

    def update(self, dt):
        self.label = self.font.render('%s' % self.score, False, self.color)


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

    score = 0

    def __init__(self):
        self.corns = LifeCorns()

    @property
    def lives(self):
        return self.corns.corns

    def set_lives(self, value):
        self.corns.corns = value

    def loose_life(self):
        self.corns.corns -= 1
