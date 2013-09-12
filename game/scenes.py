# Encoding: UTF-8

import pygame
import os
from random import randint

from game.utils import Background, Sign, Hole, Player, HighScore, HammerBlow
from game.moles import Mole, FemaleMole
from game.buttons import StartButton, CreditsButton, BackButton
from settings import fonts_dir, sounds_dir, project_dir

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


class Scene:
    background = None
    run = True
    next_scene = None
    context = None
    quit = False
    music = None

    def __init__(self, context):
        self.actors_dict = {"buttons": pygame.sprite.RenderPlain()}
        self.context = context

    def quit_event(self):
        self.run = False
        self.next_scene = None

    def keydown_event(self):
        pass

    def keyup_event(self):
        pass

    def mousemotion_event(self):
        pass

    def mousebuttonup_event(self):
        pass

    def mousebuttondown_event(self):
        pass

    def handle_events(self, event):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_event()
            elif event.type == pygame.KEYDOWN:
                self.quit_event()
                self.keydown_event()
            elif event.type == pygame.KEYUP:
                self.keyup_event()
            elif event.type == pygame.MOUSEMOTION:
                self.mousemotion_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mousebuttonup_event()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mousebuttondown_event()
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

    def reupdate(self):
        pass

    def update(self):
        self.background.update(self.context['dt'])
        for actor in self.actors_dict.values():
            actor.update(self.context['dt'])

        self.reupdate()

    def start(self):
        pass

    def loop(self):
        pass

    def set_music(self):
        if self.music[0] and self.context['music'] == 'play':
            path = os.path.join(sounds_dir, self.music[0])
            mixer.music.load(path)

    def handle_music(self):
        if self.context['music'] == 'play':
            mixer.music.stop()
            mixer.music.play(self.music[1])
        elif self.context['music'] == 'off':
            mixer.music.stop()

    def end(self):
        pass

    def play(self, clock):
        self.set_music()
        self.handle_music()
        self.start()

        while self.run:
            clock.tick(24)
            self.check_events()
            self.loop()
            self.update()
            self.draw()

        self.end()

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


class TheBugSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'bug_logo.png')
        self.next_scene = TitleScene(self.context)
        self.music = ('intro.ogg', -1)

    def end(self):
        self.context['music'] = 'on'


class FatecSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'fatec_logo.png')
        self.next_scene = TheBugSplashScene(self.context)
        self.music = ('intro.ogg', -1)

    def end(self):
        self.context['music'] = 'on'


class EndScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'end_game.png')
        self.next_scene = TitleScene(self.context)
        self.music = ('gag.mp3', 0)

    def start(self):
        font_path = os.path.join(fonts_dir, 'FreeSans.ttf')
        font = pygame.font.Font(font_path, 32)
        self.score = font.render(str(self.context['player'].score),
                                                True, (255, 255, 255))
        self.align = (440 - (self.score.get_width()))
        self.context['player'].set_lives(5)
        self.get_score()
        self.high_score = HighScore(self.context['high_score'])

    def redraw(self):
        self.context['screen'].blit(self.score, (self.align, 170))
        self.high_score.draw(self.context['screen'])

    def get_score(self):
        path = os.path.join(project_dir, 'score.txt')
        score = self.context['player'].score
        high_score = self.context['high_score']

        if score > high_score:
            score_file = open(path, 'w')
            score_file.write(str(score))
            score_file.close()
            self.context['high_score'] = score

    def end(self):
        self.context['music'] = 'play'


class TitleScene(Scene):

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background('title_screen.png')
        self.music = ('intro.ogg', -1)

    def mousebuttondown_event(self):
        position = pygame.mouse.get_pos()
        if position != (0, 0):
            for button in self.actors_dict['buttons']:
                if button.check_click(position):
                    self.run = False
                    if button.name == 'start':
                        self.next_scene = SurvivalScene(self.context)
                        self.context['music'] = 'play'
                    if button.name == 'credits':
                        self.next_scene = CreditsScene(self.context)
                        self.context['music'] = 'on'

    def start(self):
        start = StartButton()
        credits = CreditsButton()
        self.actors_dict['buttons'].add(start)
        self.actors_dict['buttons'].add(credits)
        self.high_score = HighScore(self.context['high_score'])

    def redraw(self):
        self.high_score.draw(self.context['screen'])


class CreditsScene(Scene):

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background("credits.png")
        self.music = ('intro.ogg', -1)

    def mousebuttondown_event(self):
        for button in self.actors_dict['buttons']:
            if button.check_click(pygame.mouse.get_pos()):
                self.run = False
                self.next_scene = TitleScene(self.context)

    def start(self):
        start = BackButton()
        self.actors_dict['buttons'].add(start)

    def end(self):
        self.context['music'] = 'on'


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
        self.next_scene = EndScene(self.context)
        self.music = ('mole_hole.mp3', -1)
        self.blow = HammerBlow()
        self.miss_sound = mixer.Sound(os.path.join(sounds_dir, 'cancel.ogg'))
        self.fail_sound = mixer.Sound(os.path.join(sounds_dir, 'stare.ogg'))

    def mousebuttondown_event(self):
        x, y = pygame.mouse.get_pos()

        y = (y - self.top_margin) / self.hole_height
        x = (x - self.left_margin) / self.hole_width

        hit = False
        for mole in self.actors_dict['moles']:
            if mole.coordenates == (y, x):
                self.kill_mole(mole, True)
                self.blow.play()
                hit = True
                break

        if not hit:
            self.miss_sound.play()

    def reupdate(self):
        self.score_sign.update(self.context['dt'])

    def redraw(self):
        self.score_sign.draw(self.context['screen'])
        self.context['player'].corns.draw(self.context['screen'])

    def refresh_holes(self):
        for hole in self.active_holes:
            if not hole.refresh_counter:
                self.unactive_holes.append(hole)
                self.active_holes.remove(hole)
                hole.active = False
                hole.refresh_counter = 24

    def improve_difficulty(self):
        condition = not self.context['player'].score % 100 \
                    and self.difficulty > 3 \
                    and self.context['player'].score
        if condition:
            self.difficulty -= 1

    def kill_mole(self, mole, killed=False):
        if killed:
            self.context['player'].score += mole.points
            self.improve_difficulty()
        else:
            self.context['player'].loose_life()
            self.fail_sound.play()

        self.active_holes.append(mole.hole)
        mole.hole.active = True
        mole.kill()

    def refresh_moles(self):
        for mole in self.actors_dict['moles']:
            if not mole.alive:
                self.kill_mole(mole)

    def loop(self):
        self.create_moles()
        self.refresh_moles()
        self.refresh_holes()
        self.refresh_player()
        self.score_sign.score = self.context['player'].score

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
                if randint(0, 4):
                    mole = Mole(hole.position, hole.coordenates)
                else:
                    mole = FemaleMole(hole.position, hole.coordenates)
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

    def end(self):
        self.context['music'] = 'play'
