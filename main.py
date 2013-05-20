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

    def __init__(self, score, position=(30, 100), image='sign.png'):
        GameObject.__init__(self, image, position)
        self.font = pygame.font.Font('FreeSans.ttf', 20)
        self.label_position = (position[0] + 15, position[1] + 30)
        self.score = score

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.label, self.label_position)

    def update(self, dt):
        self.label = self.font.render('Points: %s' % self.score, False, (100, 50, 0))


class LivesSign(Sign):
    def __init__(self, score, position=(300, 100), image='sign.png'):
        Sign.__init__(self, score, position, image)

    def update(self, dt):
        self.label = self.font.render('Lifes: %s' % self.score, False, (100, 50, 0))


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

    lives = 5
    score = 0


class Scene:
    background = None
    run = True
    next_scene = None

    def __init__(self, player, screen):
        self.player = player
        self.screen = screen


class EndScene(Scene):

    timer = 120

    def __init__(self, player, screen):
        Scene.__init__(self, player, screen)
        self.background = Background("end_game.png")

    def play(self, clock):
        font = pygame.font.Font('FreeSans.ttf', 60)
        score = font.render(str(self.player.score), True, (255, 255, 255))
        align = (730 - (score.get_width()))

        self.background.draw(self.screen)
        self.screen.blit(score, (align, 306))
        pygame.display.flip()

        pygame.time.delay(5000)

        return False


class SurvivalScene(Scene):
    hole_width = 128
    hole_height = 96
    top_margin = 80
    left_margin = 260
    level_map = [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]

    def __init__(self, dt, player, screen):
        Scene.__init__(self, player, screen)
        self.background = Background("background6.png")
        self.score_sign = Sign(self.player.score)
        self.lives_sign = LivesSign(self.player.lives)
        self.dt = dt

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

    def actors_update(self):
        self.background.update(self.dt)

        for actor in self.actors_dict.values():
            actor.update(self.dt)

        self.score_sign.update(self.dt)
        self.lives_sign.update(self.dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        for actor in self.actors_dict.values():
            actor.draw(self.screen)

        self.score_sign.draw(self.screen)
        self.lives_sign.draw(self.screen)

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
            self.player.lives -= 1

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
        self.score_sign.score = self.player.score
        self.lives_sign.score = self.player.lives

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
        if self.player.lives <= 0:
            self.next_scene = EndScene(self.player, self.screen)
            self.run = False

    def play(self, clock):
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
            self.handle_events()
            self.actors_update()
            self.manage()
            self.actors_draw()
            pygame.display.flip()

        return self.next_scene


class Game:

    #constantes
    screen = None
    screen_size = None
    run = True

    def __init__(self, size):

        pygame.init()

        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        self.player = Player()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Mole Hole')
        # pygame.mouse.set_visible(0)

    def loop(self):
        clock = pygame.time.Clock()
        dt = 50
        scene = SurvivalScene(dt, self.player, self.screen)

        while scene:
            scene = scene.play(clock)

        pygame.quit()


def main():
    game = Game((800, 600))
    game.loop()

if __name__ == '__main__':
    main()
