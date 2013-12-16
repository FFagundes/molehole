# Encoding: UTF-8

import pygame
import os
from random import randint

from game.utils import Background, Sign, Hole, Player, HighScore, HammerSound, HammerBlow
from game.animals import Mole, FemaleMole, CapMole, SpeedMole, Rabbit
from game.buttons import StartButton, CreditsButton, BackButton, PlayButton, NextButton
from settings import fonts_dir, sounds_dir, project_dir, frame_rate
from collections import OrderedDict

try:
    import android
except ImportError:
    android = None

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
        self.actors_dict = OrderedDict()
        self.actors_dict['buttons'] = pygame.sprite.RenderPlain()
        self.context = context

    def quit_event(self, event):
        self.run = False
        self.next_scene = None

    def keydown_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit_event(event)

    def keyup_event(self, event):
        pass

    def mousemotion_event(self, event):
        pass

    def mousebuttonup_event(self, event, position):
        pass

    def mousebuttondown_event(self, event, position):
        pass

    def handle_events(self, event):
        pass

    def check_events(self):
        if android:
            if android.check_pause():
                android.wait_for_resume()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_event(event)
            elif event.type == pygame.KEYDOWN:
                self.keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.keyup_event(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mousemotion_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                if position != (0, 0):
                    self.mousebuttonup_event(event, position)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if position != (0, 0):
                    self.mousebuttondown_event(event, position)
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
        if self.music and self.context['music'] == 'play':
            path = os.path.join(sounds_dir, self.music[0])
            mixer.music.load(path)

    def handle_music(self):
        if self.music:
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
    timer = 40

    def __init__(self, context, background):
        Scene.__init__(self, context)
        self.background = Background(background)

    def loop(self):
        if not self.timer:
            self.run = False

        self.timer -= 1

    def end(self):
        self.context['music'] = 'on'


class TheBugSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'bug_logo.png')
        self.next_scene = TitleScene(self.context)
        self.music = ('intro.ogg', -1)


class FatecSplashScene(TimerScene):
    def __init__(self, context):
        TimerScene.__init__(self, context, 'fatec_logo.png')
        self.next_scene = TheBugSplashScene(self.context)
        self.music = ('intro.ogg', -1)


class PygameSplashScene(TimerScene):
    timer = 100

    def __init__(self, context):
        TimerScene.__init__(self, context, 'pygame-presplash.jpg')
        self.next_scene = FatecSplashScene(self.context)
        self.music = ('intro.ogg', -1)


class EndScene(TimerScene):
    timer = 120

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

    def mousebuttondown_event(self, event, position):
        for button in self.actors_dict['buttons']:
            if button.check_click(position):
                self.run = False
                if button.name == 'start':
                    self.next_scene = TutorialScene1(self.context)
                    self.context['music'] = 'play'
                if button.name == 'credits':
                    self.next_scene = CreditsScene(self.context)
                    self.context['music'] = 'on'

    def start(self):
        start = StartButton()
        credits = CreditsButton()
        self.actors_dict['buttons'].add(start)
        self.actors_dict['buttons'].add(credits)
        self.high_score = HighScore(high_score=self.context['high_score'],
                                                size=22, position=(10, 287))

    def redraw(self):
        self.high_score.draw(self.context['screen'])


class TutorialScene(Scene):
    def __init__(self, context):
        Scene.__init__(self, context)

    def mousebuttondown_event(self, event, position):
        for button in self.actors_dict['buttons']:
            if button.check_click(position):
                self.run = False
                if button.name == 'play':
                    self.next_scene = SurvivalScene(self.context)
                    self.context['music'] = 'play'
                if button.name == 'next':
                    pass

    def start(self):
        play = PlayButton()
        next = NextButton()
        self.actors_dict['buttons'].add(play)
        self.actors_dict['buttons'].add(next)


class TutorialScene1(TutorialScene):

    def __init__(self, context):
        TutorialScene.__init__(self, context)
        self.background = Background('mole_hole_tuto_1.png')
        self.next_scene = TutorialScene2(context)


class TutorialScene2(TutorialScene):

    def __init__(self, context):
        TutorialScene.__init__(self, context)
        self.background = Background('mole_hole_tuto_2.png')
        self.next_scene = TutorialScene3(context)


class TutorialScene3(TutorialScene):

    def __init__(self, context):
        TutorialScene.__init__(self, context)
        self.background = Background('mole_hole_tuto_3.png')

    def start(self):
        play = PlayButton(image='btn_tuto_start_final.png')
        self.actors_dict['buttons'].add(play)


class CreditsScene(Scene):

    def __init__(self, context):
        Scene.__init__(self, context)
        self.background = Background("credits.png")
        self.music = ('intro.ogg', -1)

    def mousebuttondown_event(self, event, position):
        for button in self.actors_dict['buttons']:
            if button.check_click(position):
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
    difficulty = 20
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
        self.blow = HammerSound()
        self.miss_sound = mixer.Sound(os.path.join(sounds_dir, 'cancel.ogg'))
        self.fail_sound = mixer.Sound(os.path.join(sounds_dir, 'stare.ogg'))

    def mousebuttondown_event(self, event, (x, y)):
        cord_y = (y - self.top_margin) / self.hole_height
        cord_x = (x - self.left_margin) / self.hole_width
        hit = False

        for index in self.animals_index:
            for animal in self.actors_dict[index]:
                if animal.coordenates == (cord_y, cord_x):
                    animal.loose_life()
                    if not animal.lives:
                        self.kill_animal(animal)
                    self.blow.play()
                    hit = True
                    blow = HammerBlow((x - 25, y - 40))
                    self.actors_dict['blows'].add(blow)
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
                hole.refresh_counter = frame_rate

    def improve_difficulty(self):
        condition = not self.context['player'].score % 20 \
                    and self.context['player'].score \
                    and self.difficulty > 3
        if condition:
            self.difficulty -= 1

    def kill_animal(self, animal):
        if issubclass(type(animal), Mole):
            self.context['player'].score += animal.points
            self.improve_difficulty()
        else:
            self.context['player'].loose_life()
        animal.killed = True

    def remove_animal(self, animal):
        self.active_holes.append(animal.hole)
        animal.hole.active = True
        animal.kill()

    def refresh_animals(self):
        for mole in self.actors_dict['moles']:
            if mole.escaped:
                self.context['player'].loose_life()
                self.fail_sound.play()
                self.remove_animal(mole)
            elif mole.killed and mole.die():
                self.remove_animal(mole)

        for rabbit in self.actors_dict['rabbits']:
            if rabbit.escaped or rabbit.killed and rabbit.die():
                self.remove_animal(rabbit)

    def loop(self):
        self.create_animals()
        self.refresh_animals()
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

    def create_animals(self):
        if not randint(0, self.difficulty):
            if self.unactive_holes:
                hole_index = randint(0, len(self.unactive_holes) - 1)
                hole = self.unactive_holes[hole_index]
                rand = randint(0, 10)
                if rand == 9:
                    animal = Rabbit(hole.position, hole.coordenates)
                    self.actors_dict['rabbits'].add(animal)
                else:
                    if rand == 8:
                        animal = SpeedMole(hole.position, hole.coordenates)
                    elif rand == 7:
                        animal = CapMole(hole.position, hole.coordenates)
                    elif rand > 3:
                        animal = Mole(hole.position, hole.coordenates)
                    else:
                        animal = FemaleMole(hole.position, hole.coordenates)
                    self.actors_dict['moles'].add(animal)

                animal.hole = hole
                self.unactive_holes.remove(hole)

    def refresh_player(self):
        if self.context['player'].lives <= 0:
            self.run = False

    def add_animals_dicts(self):
        for index in self.animals_index:
            self.actors_dict[index] = pygame.sprite.RenderPlain()

    def start(self):
        self.unactive_holes = []
        self.active_holes = []
        self.actors_dict['holes'] = pygame.sprite.RenderPlain()
        self.animals_index = ('moles', 'rabbits')
        self.add_animals_dicts()
        self.actors_dict['blows'] = pygame.sprite.RenderPlain()
        self.generate_holes()

    def end(self):
        self.context['music'] = 'play'
