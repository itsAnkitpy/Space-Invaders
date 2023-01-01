import os
os.system('cls')

import pygame
import random
import math

from pygame import mixer

# Initialize the game
pygame.init()

# Create UI display
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Background of the game
background = pygame.image.load("bg.png")

# Player Settings
player_img = pygame.image.load("my_ship.png")
pos_x = 370
pos_y = 480
pos_x_change = 0

# Enemy settings

# Displaying multiple enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("ufo.png"))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
# Ready - states that we can't see the bullet on the screen
# Fire - states the bullet is currently moving
bullet_state = "ready"


score_value = 0
font = pygame.font.Font('spaceranger.ttf', 32)
textX = 10
textY = 10

# Game over
game_over_font = pygame.font.Font("spaceranger.ttf", 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_text, (200,250))

def player(x,y):
    screen.blit(player_img, (x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x,y))

def fire__bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16,y+10))
    

# Collision Detection of bullet with aliens
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt( (math.pow(enemy_x-bullet_x,2)) + (math.pow(enemy_y - bullet_y,2)) )
    if distance <= 27:
        return True
    else:
        return False

# Main gameplay loop
game_running = True

while game_running:

    screen.fill((0, 0, 0))
    # Add background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    
    # If key stroke is pressed to move the spaceship left or right
    # On key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                pos_x_change = -5
            if event.key == pygame.K_RIGHT:
                pos_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet firing sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current x coordinate of our spaceship
                    bullet_x = pos_x
                    fire__bullet(bullet_x, bullet_y)

        # On key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pos_x_change = 0

    # Defining the boundaries for the spaceship movement
    if pos_x <= 0:
        pos_x = 0
    elif pos_x >= 736:
        pos_x = 736

    # Defining the boundaries for the enemy movement and its movement downwards
    for i in range(num_of_enemies):

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break


        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >=736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Collision of bullet with aliens
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            # Collision sound
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()

            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0,800)
            enemy_y[i] = random.randint(50,150)

        enemy(enemy_x[i],enemy_y[i],i)
 
 

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state  = "ready"

    if bullet_state == "fire":
        fire__bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    
    pos_x += pos_x_change
    

    player(pos_x,pos_y)
    show_score(textX,textY)
    pygame.display.update()