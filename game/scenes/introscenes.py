from scenes import Scene, TitleScene
from game.utils import Background
import pygame


class IntroScene(Scene):
    timer = 120

    def __init__(self, context, background):
        Scene.__init__(self, context)
        self.background = Background(background)

    def loop(self):
        self.handle_events()
        if not self.timer:
            self.run = False

        self.timer -= 1

    def start(self):
        self.background.draw(self.context['screen'])
        pygame.display.update()


class TheBugSplashScene(IntroScene):
    def __init__(self, context):
        IntroScene.__init__(self, context, 'bug_logo.png')
        self.next_scene = TitleScene(self.context)


class FatecSplashScene(IntroScene):
    def __init__(self, context):
        IntroScene.__init__(self, context, 'fatec_logo.png')
        self.next_scene = TheBugSplashScene(self.context)
