# Encoding: UTF-8

# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu


import pygame
from random import randint


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


def get_event(done):
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = (x - 80) / 128
            y = (y - 260) / 96

            for hole in holes:
                hole['is_clicked'] = False
                if hole['cel'] == (x, y) and hole['is_active'] == True:
                    hole['is_clicked'] = True
                    return 'point'

        elif event.type == pygame.MOUSEMOTION:
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
        if hole['is_active'] == True:
            tabuleiro.blit(mole_active, hole['position'])

        if hole['is_clicked']:
            tabuleiro.blit(mole_punk, hole['position'])
            hole['is_active'] = False


def draw_hole(hole, color):
    pygame.draw.rect(tabuleiro, color, (hole['position'][0], hole['position'][1], 128, 96))


def clear_click():
    for hole in holes:
        hole['is_clicked'] = False


def active_mole(hole):
    if hole['mole_timer']:
        hole['is_active'] = True


def verify_holes(mole_counter):
    # fail = False
    for hole in holes:
        if hole['mole_timer'] and hole['is_active'] == True:
            hole['mole_timer'] -= 1

        else:
        # elif not hole['mole_timer']:
        #     fail = True
            hole['is_active'] = False
            hole['inactive_time'] -= 1

            if not hole['inactive_time']:
                hole['mole_timer'] = 40
                hole['inactive_time'] = 20

        # if fail:
        #     mole_counter += 1
        #     return mole_counter
        # else:
        #     return 0


# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (41, 180, 49)
red = (255, 0, 0)
alpha = (0, 0, 0, 0)

pygame.init()

# Inicializa os valores
holes = create_holes()

screen = pygame.display.set_mode((800, 600))
tabuleiro = pygame.Surface((640, 288), flags=pygame.SRCALPHA)
martelo = pygame.Surface((800, 600), flags=pygame.SRCALPHA)

background = pygame.image.load('images/background.png')
hole_bg = pygame.image.load('images/hole_0.png')
mole_active = pygame.image.load('images/mole.png')
mole_punk = pygame.image.load('images/mole_punk.png')
hammer = pygame.image.load('images/hammer.png')

pygame.display.set_caption("Mole Hole")

points = 0
mole_counter = 0

points_font = pygame.font.SysFont('tahoma', 24, bold=True)


#Eventos iniciais
alive_holes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
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
while done == False:

    pygame.mouse.set_visible(False)

    tabuleiro.fill(alpha)
    clear_click()
    done = get_event(done)
    if done == 'point':
        points = add_point(points)
        done = False

    # Set the screen background
    screen.fill(black)

    if randint(0, 10) == 1:
        active_mole(holes[randint(0, 14)])

    mole_counter = verify_holes(mole_counter)

    # Limit to 20 frames per second
    clock.tick(20)

    draw_holes()

    point_render = points_font.render(('Points  ' + str(points)), True, (255, 255, 255))
    screen.blit(background, (0, 0))
    screen.blit(tabuleiro, (80, 260))
    screen.blit(point_render, (650, 20))
    screen.blit(martelo, (0, 0))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
