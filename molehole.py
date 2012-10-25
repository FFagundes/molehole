# Encoding: UTF-8

# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu


import pygame
from random import randint

try:
    import android
except ImportError:
    android = None

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


def create_holes():
    holes = []
    width = 128
    height = 96

    for x in range(3):
        for y in range(5):
            holes.append(
                    {
                        'cel': (y, x),
                        'position': (y * width, x * height),
                        'is_alive': False,
                        'is_active': False,
                        'is_clicked': False,
                        'mole_timer': 40,
                        'inactive_time': 60,
                    }

            )

    return holes


def place_holes(alive_holes):
    for hole in alive_holes:
        holes[hole]['is_alive'] = True


def kreturn_press():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return True

        elif event.type == pygame.QUIT:
            return True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            return True

    return False


def get_event(done):
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            martelo.fill(alpha)
            martelo.blit(hammer2, (x - 30, y - 40))

            x = (x - 80) / 128
            y = (y - 260) / 96

            for hole in holes:
                hole['is_clicked'] = False
                if hole['cel'] == (x, y) and hole['is_active'] == True:
                    hole['is_clicked'] = True
                    return 'point'

            return 'miss'

        elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            martelo.fill(alpha)
            martelo.blit(hammer, (x - 30, y - 40))

    return done


def add_point(points):
    points += 1
    return points


def draw_holes():
    for hole in holes:
        if hole['is_alive']:
            tabuleiro.blit(hole_bg, hole['position'])

        if hole['is_clicked']:
            topeiras.blit(mole_punk, hole['position'])
            topeiras.blit(stars, hole['position'])
            hole['is_active'] = False

        elif hole['is_active'] == True:
            topeiras.blit(mole_active, hole['position'])


def draw_hole(hole, color):
    pygame.draw.rect(tabuleiro, color, (hole['position'][0], hole['position'][1], 128, 96))


def clear_click():
    for hole in holes:
        hole['is_clicked'] = False


def active_hole(hole):
    if hole['mole_timer'] and hole['is_alive']:
        hole['is_active'] = True


def randomize(pudim):
    if randint(0, 100) < pudim[1]:
        random = randint(1, 13)
        while random not in alive_holes:
            random = randint(1, 13)
        active_hole(holes[random])

    if pudim[0] < 300:
        pudim[0] = pudim[0] + 1
    else:
        pudim[1] = pudim[1] + 1
        pudim[0] = 0

    return pudim


def verify_holes(lifes):
    fail = False
    for hole in holes:
        if hole['mole_timer'] and hole['is_active'] == True:
            hole['mole_timer'] -= 1

        else:

            if hole['is_active'] == True:
                fail = True

            hole['is_active'] = False
            hole['inactive_time'] -= 1

            if not hole['inactive_time']:
                hole['mole_timer'] = 40
                hole['inactive_time'] = 20

    if fail:
        lifes -= 1
        life_lost.play()

    return lifes


def verify_lifes():
    pass


# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (41, 180, 49)
red = (255, 0, 0)
alpha = (0, 0, 0, 0)

pygame.init()

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

mixer.init()
mixer.music.load('sounds/wooly_bully.mp3')
if android:
    mixer.music.play()
    mixer.periodic()
else:
    mixer.music.play(-1)

blow1 = mixer.Sound('sounds/blow1.ogg')
blow2 = mixer.Sound('sounds/blow2.ogg')
blow3 = mixer.Sound('sounds/blow3.ogg')
blow4 = mixer.Sound('sounds/blow4.ogg')
miss = mixer.Sound('sounds/cancel.ogg')
life_lost = mixer.Sound('sounds/stare.ogg')

# Inicializa os valores
holes = create_holes()

screen = pygame.display.set_mode((800, 600))
tabuleiro = pygame.Surface((640, 288), flags=pygame.SRCALPHA)
topeiras = pygame.Surface((640, 288), flags=pygame.SRCALPHA)
martelo = pygame.Surface((800, 600), flags=pygame.SRCALPHA)

background = pygame.image.load('images/background.png')
flare = pygame.image.load('images/flare.png')
hole_bg = pygame.image.load('images/hole1.png')
mole_active = pygame.image.load('images/mole1.png')
mole_punk = pygame.image.load('images/mole3.png')
stars = pygame.image.load('images/stars.png')
stars.set_alpha(True)
hammer = pygame.image.load('images/hammer.png')
hammer2 = pygame.image.load('images/hammer2.png')

pygame.display.set_caption("Mole Hole")
pygame.mouse.set_visible(False)

points = 0
lifes = 5
speed_counter = 0
dificulty = 8

title_font = pygame.font.Font('FreeSans.ttf', 50)
points_font = pygame.font.Font('FreeSans.ttf', 24)
lifes_font = pygame.font.Font('FreeSans.ttf', 24)
points_font.set_bold(True)
dead_title_font = pygame.font.Font('FreeSans.ttf', 50)
dead_points_font = pygame.font.Font('FreeSans.ttf', 140)


#Eventos iniciais
alive_holes = [1, 2, 3, 6, 7, 8, 11, 12, 13]
place_holes(alive_holes)


# Variáveis de controle
frame_count = 0
buraco = False
mole_time = 60


#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# -------- Main Program Loop -----------

title_render = title_font.render(('Iniciar'), True, (255, 150, 0))
title_align = (400 - (title_render.get_width() / 2))

screen.fill(black)
screen.blit(title_render, (title_align, 450))
pygame.display.flip()

while not kreturn_press():
    clock.tick(20)


while not done:

    # Limit to 20 frames per second
    clock.tick(20)

    tabuleiro.fill(alpha)
    topeiras.fill(alpha)
    clear_click()
    done = get_event(done)
    if done == 'point':
        blow_number = randint(0, 3)
        if blow_number == 0:
            blow1.play()
        elif blow_number == 1:
            blow2.play()
        elif blow_number == 2:
            blow3.play()
        elif blow_number == 3:
            blow4.play()
        points = add_point(points)
        done = False

    if done == 'miss':
        miss.play()
        done = False

    # Set the screen background
    screen.fill(black)

    # speed_counter = randomize(speed_counter)
    (speed_counter, dificulty) = randomize([speed_counter, dificulty])

    lifes = verify_holes(lifes)
    if lifes == 0:
        done = True

    draw_holes()

    points_render = points_font.render(str(points), True, (178, 34, 34))
    lifes_render = lifes_font.render(('Lifes  ' + str(lifes)), True, (0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(tabuleiro, (80, 260))
    screen.blit(topeiras, (80, 260))
    screen.blit(points_render, (686, 132))
    screen.blit(lifes_render, (600, 20))
    screen.blit(martelo, (0, 0))
    screen.blit(flare, (0, 0))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.


dead_title_render = dead_title_font.render(('PONTOS'), True, (255, 255, 255))
dead_title_align = (400 - (dead_title_render.get_width() / 2))

dead_points_render = dead_points_font.render(str(points), True, (255, 255, 255))
dead_points_align = (400 - (dead_points_render.get_width() / 2))

pygame.mouse.set_visible(True)

screen.fill(black)
screen.blit(dead_title_render, (dead_title_align, 130))
screen.blit(dead_points_render, (dead_points_align, 230))
pygame.display.flip()

while not kreturn_press():
    clock.tick(20)

pygame.quit()
