# import libraries
import random
import pygame
import os

# init pygame
pygame.init()

# game window dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Boaty')

# pos for middles
MIDDLE_WIDTH = SCREEN_WIDTH // 2 - 10
MIDDLE_HEIGHT = SCREEN_HEIGHT // 2

# set frame rate
clock = pygame.time.Clock()
FPS = 60

rotate = 270

# game vars
VEL = 2.5
dx = MIDDLE_WIDTH
dy = MIDDLE_HEIGHT
score = 0
BOAT_WIDTH, BOAT_HEIGHT = 32, 32
BORDER = pygame.Rect(SCREEN_WIDTH // 2 - 5, 0, 10, SCREEN_HEIGHT)
trash = random.randrange(1, 3)
screen_rand_spot_width = random.randint(32, 568)
screen_rand_spot_height = random.randint(32, 268)

# load images
bg_image = pygame.image.load('ocean.jpg').convert_alpha()
stink_image = pygame.transform.scale(pygame.image.load('stink.png').convert_alpha(), (35, 35))
plastic_image = pygame.transform.scale(pygame.image.load('plastic-bag.png').convert_alpha(), (30, 30))
water_image = pygame.transform.scale(pygame.image.load('water.png').convert_alpha(), (30, 30))
stink = 1
plastic = 2
water = 3

if os.path.exists('high_score.txt'):
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)


# function for output text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing bg
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


run = True
while run:

    clock.tick(FPS)

    boat = pygame.Rect(dx, dy, BOAT_WIDTH, BOAT_HEIGHT)
    trash_rect = pygame.Rect(screen_rand_spot_width, screen_rand_spot_height, 32, 32)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and boat.x - VEL > 0:  # LEFT
        dx -= VEL
        rotate = 0
    if keys_pressed[pygame.K_d] and boat.x + VEL < 555:  # RIGHT
        dx += VEL
        rotate = 180
    if keys_pressed[pygame.K_w] and boat.y - VEL > 0:  # UP
        dy -= VEL
        rotate = 270
    if keys_pressed[pygame.K_s] and boat.y + VEL + boat.height < SCREEN_HEIGHT - 15:  # DOWN
        dy += VEL
        rotate = 90

    boat_image = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load('boat.png').convert_alpha(), (45, 45)),
        rotate)

    bg_scroll = 0

    draw_bg(bg_scroll)


    if trash == 1:
        screen.blit(water_image, (screen_rand_spot_width, screen_rand_spot_height))
    if trash == 2:
        screen.blit(plastic_image, (screen_rand_spot_width, screen_rand_spot_height))
    if trash == 3:
        screen.blit(stink_image, (screen_rand_spot_width, screen_rand_spot_height))

    # collision checks
    if pygame.Rect.colliderect(boat, trash_rect):
        trash = random.randint(1, 3)
        score += 1
        print(score)
        screen_rand_spot_width = random.randint(32, 568)
        screen_rand_spot_height = random.randint(32, 268)
        water_image = random.choice([plastic_image, stink_image])
        plastic_image = random.choice([water_image, stink_image])
        stink_image = random.choice([water_image, plastic_image])

    # draw img
    screen.blit(boat_image, (dx, dy))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # update high score
            if score > high_score:
                high_score = score
                with open('high_score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False
    # update display
    pygame.display.update()

pygame.quit()
