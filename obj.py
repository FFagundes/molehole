# Encoding: UTF-8

import os
import sys
import getopt

import pygame

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

    active = True

    def __init__(self, position, image):
        GameObject.__init__(self, image, position)

    def update(self, dt):
        if not self.active:
            self.image = None


class Game:
    screen = None
    screen_size = None
    run = True
    actors_dict = None
    background = None
    level_map = [
                    [0, 0, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 0, 1, 0],
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
        pass

    def generate_holes(self):
        for (x, lin) in enumerate(self.level_map):
            for (y, col) in enumerate(lin):
                if col:
                    hole = Hole(
                        ((y * 128) + 80, (x * 96) + 260),
                        "hole1.png")
                    self.actors_dict['holes'].add(hole)

    def loop(self):
        self.background = Background("background.png")
        clock = pygame.time.Clock()
        dt = 50
        self.interval = 1
        self.actors_dict = {
            "holes": pygame.sprite.RenderPlain(),
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

            print "FPS: %0.2f" % clock.get_fps()


def main():
    game = Game((800, 600))
    game.loop()

if __name__ == '__main__':
    main()
