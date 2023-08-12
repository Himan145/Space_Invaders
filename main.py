import random
import math

import pygame
from pygame import mixer

# initialize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))  # width and height
# background
background = pygame.image.load('dark-red-water-with-foam (1).jpg')

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('seafood (1).png')
pygame.display.set_icon(icon)

# background music
mixer.music.load('bensound-summer_mp3_music.mp3')
mixer.music.play(-1)

# player image
playerimg = pygame.image.load('space-invaders.png')
playerx = 350  # 350 from left
playery = 500  # 400 from top
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
number_of_enemy = 5
for i in range(number_of_enemy):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 734))  # by reloading it can be any position of 0 to 734
    enemyy.append(random.randint(50, 100))
    enemyx_change.append(0.7)
    enemyy_change.append(30)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 500
bulletx_change = 0
bullety_change = 3
bullet_state = "ready"

# count score
score = 0
font = pygame.font.Font('freesansbold.ttf', 35)

textx = 10
texty = 10


def show_score(x, y):
    updated_score = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(updated_score, (x, y))


game_over_font = pygame.font.Font('freesansbold.ttf', 70)


def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (180, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx) * (ex - bx) + (ey - by) * (ey - by))
    if (distance < 27):
        return True
    else:
        return False


# game loop
running = True
while running:
    # screen color
    screen.fill((0, 50, 0))  # (r,g,b)
    # background img
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.9
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('mixkit-big-fire-magic-swoosh-1327.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0;

    playerx = playerx + playerx_change
    # condition for not going outside screen
    # player
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:  # (800-64)=736 ,64 for size of player
        playerx = 736

    # enemy movment
    for i in range(number_of_enemy):

        # game over
        if enemyy[i] > 350:
            for j in range(number_of_enemy):
                enemyy[j] = 2000
            playery = 2000
            bullety = 2000
            game_over()
            break

        # game running
        enemyx[i] = enemyx[i] + enemyx_change[i]
        # when hit boundry it move reverse
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.7
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.7
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            colli_sound = mixer.Sound('mixkit-fuel-explosion-1705.wav')
            colli_sound.play()
            bullety = 400
            bullet_state = "ready"
            score += 1
            # print(score)
            # after collision enemy will be restart from any random position
            enemyx[i] = random.randint(0, 734)  # by reloading it can be any position of 0 to 734
            enemyy[i] = random.randint(50, 100)

        # enemy function call
        enemy(enemyx[i], enemyy[i], i)

    # bullet movment
    if bullety <= 0:
        bullety = 400
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet_fire(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()  # updating by new upper operation
