# Encoding: UTF-8

import pygame
from game.scenes import FatecSplashScene

try:
    import android
except ImportError:
    android = None


class Game(object):

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

        self.screen = pygame.display.set_mode(size)
        self.purge()
        # pygame.mouse.set_visible(0)

    def get_high_score(self):
        try:
            score_file = open('score.txt', 'r+')
            high_score = int(score_file.read())
        except (IOError, ValueError):
            high_score = 0

        return high_score

    def loop(self):
        clock = pygame.time.Clock()
        context = {'dt': 50,
                    'screen': self.screen,
                    'music': 'play',
                    'high_score': self.get_high_score()}
        scene = FatecSplashScene(context)

        while scene:
            scene = scene.play(clock)

        pygame.quit()


def main():
    game = Game((480, 320))
    game.loop()

if __name__ == '__main__':
    main()
