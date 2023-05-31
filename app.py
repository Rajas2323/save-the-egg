import math
import random
import pygame
import time
from pygame import mixer

pygame.init()
rand = random.SystemRandom()

window = pygame.display.set_mode((0, 0))

mixer.music.load("music.wav")
mixer.music.play(-1)
bomb = False
gift = False
lives = 6
score = 0
move_left = False
move_right = False
screenx, screeny = window.get_size()
playerx = screenx / 2 - 70
playery = screeny - 100
bonusx = rand.randint(0, screenx - 10)
bonusy = rand.randint(-250, 0)
eggx = random.randint(0, screenx - 10)
eggy = 0
bombx = random.randint(0, screenx - 10)
bomby = rand.randint(-250, 0)
egg_image = pygame.image.load("egg.png")
egg_image = pygame.transform.scale(egg_image, (50, 50))
basket = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket, (100, 100))
background = pygame.image.load("background2.jpg")
fruit = pygame.image.load("fruit.png")
bomb_image = pygame.image.load("bomb.png")
background = pygame.transform.scale(background, (screenx, screeny))
font_score = pygame.font.Font("freesansbold.ttf", 50)
font_lives = pygame.font.Font("freesansbold.ttf", 50)
font_over = pygame.font.Font("freesansbold.ttf", 80)
gift_stopper = None
bomb_stopper = None
over = False

clock = pygame.time.Clock()
dt = clock.tick(200) / 1000


def game_over():
    over_text = font_over.render("GAME OVER", True, (255, 0, 0))
    window.blit(over_text, (screenx/2 - 240, screeny / 2))


def bomber(x, y):
    window.blit(bomb_image, (x, y))


def bonus(x, y):
    window.blit(fruit, (x, y))


def show_score(x, y):
    score_render = font_score.render(f"Score: {score}", True, (0, 255, 0))
    window.blit(score_render, (x, y))


def show_lives(x, y):
    lives_render = font_lives.render(f"Lives: {lives}", True, (0, 0, 255))
    window.blit(lives_render, (x, y))


def player(x, y):
    window.blit(basket, (x, y))


def collision(object_1, object_2):
    # distance = math.sqrt(math.pow(object_1[0] - object_2[0], 2) + math.pow(object_1[1] - object_2[1], 2))

    if object_1[0] - object_2[0] <= 52 and object_1[0] - object_2[0] >= -70:
        if object_1[1] - object_2[1] <= 25 and object_1[1] - object_2[1] >= -25:
            if object_1[1] <= screeny - 100:
                return True

    # if distance <= 50:
    #     return True
    return False


running = True
changex = 800
fall = random.randint(150, 250)
fall2 = random.randint(150, 250)


class Egg:
    egg_image = pygame.image.load("egg.png")
    egg_image = pygame.transform.scale(egg_image, (50, 50))
    eggx = rand.randint(2, screenx - 50)
    eggy = rand.randint(-100, 100)

    def __int__(self):
        ...

    def create(self):
        window.blit(self.egg_image, (self.eggx, self.eggy))

    def fall_speed(self, speed):
        self.eggy += speed * dt

    def replace(self, x, y):
        self.eggx = x
        self.eggy = y
        fall = random.randint(70, 150)
        anda.fall_speed(fall)


anda = Egg()
anda.eggx = rand.randint(5, screenx - 10)
anda.fall_speed(rand.randint(80, 230))
anda2 = Egg()
anda2.eggx = rand.randint(1, screenx - 20)
anda.fall_speed(rand.randint(100, 200))

while running:
    if not over:
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        if playerx <= 10:
            playerx = 11

        if playerx >= screenx - 110:
            playerx = screenx - 109

        if anda.eggy > screeny - 40:
            egg_crash = mixer.Sound("crash.wav")
            egg_crash.play()
            anda.replace(rand.randint(2, screenx - 100), rand.randint(-250, 15))
            lives -= 1

        if anda2.eggy > screeny - 40:
            egg_crash = mixer.Sound("crash.wav")
            egg_crash.play()
            anda2.replace(rand.randint(2, screenx - 100), rand.randint(-180, -90))
            lives -= 1

        if anda.eggy < 50 and anda2.eggy < 50 and anda.eggy - anda2.eggy <= 30:
            anda.replace(rand.randint(2, screenx - 100), rand.randint(-180, -90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_LEFT:
                    move_left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

        if move_left and not move_right:
            playerx -= changex * dt

        elif move_right and not move_left:
            playerx += changex * dt

        if collision((playerx, playery), (anda.eggx, anda.eggy)):
            egg_catch = mixer.Sound("catch.wav")
            egg_catch.play()
            anda.replace(rand.randint(2, screenx - 100), rand.randint(-180, -90))
            score += 10

        if collision((playerx, playery), (anda2.eggx, anda2.eggy)):
            egg_catch = mixer.Sound("catch.wav")
            egg_catch.play()
            anda2.replace(rand.randint(2, screenx - 100), rand.randint(-250, 15))
            score += 10

        if score != 0 and score % 40 == 0 and score != gift_stopper:
            gift_stopper = score
            gift = random.choice([True, False])

        if gift:
            bonusy += 150 * dt

        if collision((playerx, playery), (bonusx, bonusy)) and gift:
            bonus_sound = mixer.Sound("bonus.wav")
            bonus_sound.play()
            gift = False
            lives += rand.randint(2, 4)
            bonusx = rand.randint(2, screenx - 40)
            bonusy = rand.randint(-250, -50)

        if bonusy > screeny - 40:
            gift_miss = mixer.Sound("gift_fail.wav")
            gift_miss.play()
            gift = False
            bonusx = rand.randint(2, screenx - 40)
            bonusy = rand.randint(-250, -50)

        if score % 40 == 0 and score != bomb_stopper:
            bomb = True
            bomb_stopper = score

        if bomb:
            bomby += 180 * dt

        if collision((playerx, playery), (bombx, bomby)) and bomb:
            blast = mixer.Sound("blast.wav")
            blast.play()
            bomb = False
            lives -= 1
            bombx = rand.randint(2, screenx - 40)
            bomby = rand.randint(-250, -50)

        if bomby > screeny - 40 and bomb:
            bomb = False
            bombx = rand.randint(2, screenx - 40)
            bomby = rand.randint(-250, -50)

        if lives < 0:
            over = True

        anda2.create()

        anda2.fall_speed(fall2)
        anda.fall_speed(fall)
        anda.create()
        bomber(bombx, bomby)
        bonus(bonusx, bonusy)

        player(playerx, playery)
        show_score(15, 15)
        show_lives(screenx - 200, 15)

        pygame.display.update()

    else:
        mixer.music.stop()
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        game_over()
        pygame.display.update()
