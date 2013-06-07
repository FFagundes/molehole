# Encoding: UTF-8

import pygame
from random import randint

from game.utils import Background, Sign, LivesSign, Hole, Player
from game.moles import Mole
from game.buttons import Button


class Scene:
    background = None
    run = True
    next_scene = None
    context = None
    quit = False

    def __init__(self, context):
        self.actors_dict = {"buttons": pygame.sprite.RenderPlain()}
        self.context = context

    def handle_events(self, event):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.next_scene = None
            else:
                self.handle_events(event)

    def redraw(self):
        pass

    def draw(self):
        self.background.draw(self.context['screen'])
        for actor in self.actors_dict.values():
            actor.draw(self.context['screen'])

        self.redraw()
        pygame.display.update()

    def start(self):
        pass

    def loop(self):
        pass

    def play(self, clock):
        self.start()

        while self.run:
            clock.tick(24)
            self.check_events()
            self.loop()
            self.draw()

        return self.next_scene


class TimerScene(Scene):
    timer = 120

    def __init__(self, context, background):
        Scene.__init__(self, context)
        self.background = Background(background)

    def loop(self):
        if not self.timer:
            self.run = False

        self.timer -= 1

    def start(self):
        self.background.draw(self.context['screen'])
        pygame.display.update()


class TheBugSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'bug_logo.png')
        self.next_scene = TitleScene(self.context)


class FatecSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'fatec_logo.png')
        self.next_scene = TheBugSplashScene(self.context)


class EndScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'end_game.png')
        self.next_scene = TitleScene(self.context)

    def start(self):
        font = pygame.font.Font('FreeSans.ttf', 32)
        self.score = font.render(str(self.context['player'].score),
                                                True, (255, 255, 255))
        self.align = (440 - (self.score.get_width()))
        self.context['player'].lives = 5
        self.context['player'].lives = 5

    def redraw(self):
        self.context['screen'].blit(self.score, (self.align, 170))


class TitleScene(Scene):

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background('title_screen.png')

    def click_event(self):
        for button in self.actors_dict['buttons']:
            if button.check_click(pygame.mouse.get_pos()):
                self.run = False
                self.next_scene = SurvivalScene(self.context)

    def handle_events(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_event()

    def start(self):
        start = Button((65, 140), 'btn_start.png')
        self.actors_dict['buttons'].add(start)


class SurvivalScene(Scene):
    hole_width = 86
    hole_height = 73
    left_margin = 13
    top_margin = 96
    level_map = [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background("background.png")
        self.context['player'] = Player()
        self.score_sign = Sign(self.context['player'].score)
        self.lives_sign = LivesSign(self.context['player'].lives)
        self.next_scene = EndScene(self.context)

    def click_event(self):
        x, y = pygame.mouse.get_pos()

        y = (y - self.top_margin) / self.hole_height
        x = (x - self.left_margin) / self.hole_width

        for mole in self.actors_dict['moles']:
            if mole.coordenates == (y, x):
                self.kill_mole(mole, True)

    def handle_events(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_event()

    def actors_update(self):
        self.background.update(self.context['dt'])

        for actor in self.actors_dict.values():
            actor.update(self.context['dt'])

        self.score_sign.update(self.context['dt'])
        self.lives_sign.update(self.context['dt'])

    def redraw(self):
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
            self.context['player'].score += mole.points
        else:
            self.context['player'].lives -= 1

        self.active_holes.append(mole.hole)
        mole.hole.active = True
        mole.kill()

    def refresh_moles(self):
        for mole in self.actors_dict['moles']:
            if not mole.alive:
                self.kill_mole(mole)

    def loop(self):
        self.actors_update()
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

                    hor_align = (y * self.hole_width) +\
                                        self.left_margin + (y * 6)
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
            self.run = False

    def start(self):
        self.difficulty = 10
        self.unactive_holes = []
        self.active_holes = []
        self.actors_dict['holes'] = pygame.sprite.RenderPlain()
        self.actors_dict['moles'] = pygame.sprite.RenderPlain()
        self.generate_holes()
