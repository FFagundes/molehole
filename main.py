# Encoding: UTF-8

import os
import sys
import getopt

import pygame

from random import randint

try:
    import android
    images_dir = os.path.join("")
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

    def __init__(self, score, position=(175, 33), image='sign.png'):
        GameObject.__init__(self, image, position)
        self.font = pygame.font.Font('FreeSans.ttf', 16)
        self.label_position = (position[0] + 10, position[1] + 13)
        self.score = score

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.label, self.label_position)

    def update(self, dt):
        self.label = self.font.render('Score: %s' % self.score, False, (100, 50, 0))


class LivesSign(Sign):
    def __init__(self, score, position=(360, 20), image='sign.png'):
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
    alive_timer = 25
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
    context = None
    quit = False

    def __init__(self, context):
        self.context = context

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.quit = True


class EndScene(Scene):

    timer = 120

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background("end_game.png")

    def play(self, clock):
        font = pygame.font.Font('FreeSans.ttf', 32)
        score = font.render(str(self.context['player'].score), True, (255, 255, 255))
        align = (440 - (score.get_width()))

        self.background.draw(self.context['screen'])
        self.context['screen'].blit(score, (align, 170))
        pygame.display.update()

        pygame.time.delay(5000)

        return False


class IntroScene(Scene):

    timer = 120

    def __init__(self, context):
        Scene.__init__(self, context)
        self.fase = 0

    def first_screen(self):
        self.background = Background("fatec_logo.png")
        self.background.draw(self.context['screen'])
        pygame.display.update()

    def second_screen(self):
        self.background = Background("bug_logo.png")
        self.background.draw(self.context['screen'])
        pygame.display.update()

    def loop(self):
        self.handle_events()
        if not self.timer and self.fase == 0:
            self.second_screen()
            self.fase = 1
            self.timer = 120
            return

        elif not self.timer and self.fase == 1:
            self.run = False

        self.timer -= 1

    def play(self, clock):
        self.first_screen()

        while self.run:
            clock.tick(24)
            self.loop()

        if self.quit:
            return False

        return SurvivalScene(self.context)


class SurvivalScene(Scene):
    hole_width = 81
    hole_height = 73
    left_margin = 24
    top_margin = 96
    level_map = [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background("background.png")
        self.score_sign = Sign(self.context['player'].score)
        self.lives_sign = LivesSign(self.context['player'].lives)

    def click_event(self):
        x, y = pygame.mouse.get_pos()

        y = (y - self.top_margin) / self.hole_height
        x = (x - self.left_margin) / self.hole_width

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
        self.background.update(self.context['dt'])

        for actor in self.actors_dict.values():
            actor.update(self.context['dt'])

        self.score_sign.update(self.context['dt'])
        self.lives_sign.update(self.context['dt'])

    def actors_draw(self):
        self.background.draw(self.context['screen'])
        for actor in self.actors_dict.values():
            actor.draw(self.context['screen'])

        self.score_sign.draw(self.context['screen'])
        self.lives_sign.draw(self.context['screen'])

    def refresh_holes(self):
        for hole in self.active_holes:
            if not hole.refresh_counter:
                self.unactive_holes.append(hole)
                self.active_holes.remove(hole)
                hole.active = False
                hole.refresh_counter = 24

    def kill_mole(self, mole, killed=False):
        if killed:
            self.context['player'].score += 1
        else:
            self.context['player'].lives -= 1

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
        self.score_sign.score = self.context['player'].score
        self.lives_sign.score = self.context['player'].lives

    def generate_holes(self):
        for (x, lin) in enumerate(self.level_map):
            for (y, col) in enumerate(lin):
                if col:

                    hor_align = (y * self.hole_width) + self.left_margin + (y * 6)
                    ver_align = (x * self.hole_height) + self.top_margin

                    hole = Hole((hor_align, ver_align), "hole.png", (x, y))

                    self.actors_dict['holes'].add(hole)
                    self.unactive_holes.append(hole)

    def create_moles(self):

        if not randint(0, self.difficulty):
            if self.unactive_holes:
                hole_index = randint(0, len(self.unactive_holes) - 1)
                hole = self.unactive_holes[hole_index]

                mole = Mole(hole.position, "mole.png", hole.coordenates)
                self.actors_dict['moles'].add(mole)
                mole.hole = hole
                self.unactive_holes.remove(hole)

    def refresh_player(self):
        if self.context['player'].lives <= 0:
            self.next_scene = EndScene(self.context)
            self.run = False

    def play(self, clock):
        self.difficulty = 10
        self.unactive_holes = []
        self.active_holes = []
        self.actors_dict = {
            "holes": pygame.sprite.RenderPlain(),
            "moles": pygame.sprite.RenderPlain(),
            }

        self.generate_holes()

        while self.run:
            clock.tick(24)
            self.handle_events()
            self.actors_update()
            self.manage()
            self.actors_draw()
            pygame.display.update()

        return self.next_scene


class Game:

    #constantes
    screen = None
    screen_size = None
    run = True

    def purge(self):
        """Necessary to clear the flash screen buffer"""
        pygame.display.update()
        pygame.display.update()

    def __init__(self, size):

        pygame.init()
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        self.player = Player()
        self.screen = pygame.display.set_mode(size)
        self.purge()
        # pygame.mouse.set_visible(0)

    def loop(self):
        clock = pygame.time.Clock()
        context = {'dt': 50, 'player': self.player, 'screen': self.screen}
        scene = IntroScene(context)

        while scene:
            scene = scene.play(clock)

        pygame.quit()


def main():
    game = Game((480, 320))
    game.loop()

if __name__ == '__main__':
    main()
