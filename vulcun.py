# coding=utf-8
"""
EXAMPLE 1
Example file, timer clock with in-menu options.
Copyright (C) 2017-2018 Pablo Pizarro @ppizarror
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

#import plane24
#from plane25 import go
# Import pygame and libraries
import random
from random import randrange
import time
import datetime
import os
import pygame
from pygame.locals import *
from score import getScore
from score import writescore

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# -----------------------------------------------------------------------------
# Constants and global variables
ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
SCORES = ['100','200']
W_SIZE = 800  # Width of window size



# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
for m in HELP:
    print(m)

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('PygameMenu example')

# Main timer and game clock
clock = pygame.time.Clock()
timer = [0.0]
dt = 1.0 / FPS
timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)


# -----------------------------------------------------------------------------

def go():

    WIDTH = 800
    HEIGHT = 800
    fps = 60

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    #set up assets (art and sounds)
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    snd_dir = os.path.join(game_folder, 'snd')

    running = True
    #create python class
    pygame.init()

    #sounds
    pygame.mixer.init()

    #screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #caption
    pygame.display.set_caption('my game')

    #clock
    clock = pygame.time.Clock()

    #display score
    font_name = pygame.font.match_font("arial")

    #score
    score = 0

    #shield
    shield = 3
    shield_name = ''


    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


    class Plane(pygame.sprite.Sprite):
        # sprite for the Player
        # __init__ what code to run when creating class sprite
        def __init__(self):
            # this line is required to properly create the sprite
            pygame.sprite.Sprite.__init__(self)
            # create a plain rectangle for the sprite image
            #self.image = pygame.Surface((50, 50))
            self.image = pygame.image.load(os.path.join(img_folder, 'plane2.xcf')).convert()
            #self.image.fill(GREEN)
            # find the rectangle that encloses the image
            self.rect = self.image.get_rect()
            # center the sprite on the screen
            self.rect.top = 10
            self.speedx = 0
            self.shield = 20

        def update(self):

            # moving motion
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
                #self.movel(-5)
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
                #self.mover(5)

            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

    class Missile(pygame.sprite.Sprite):

        def __init__(self, t, u):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((5, 40))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.centerx = t
            self.rect.centery = u
            self.speedy = +10

        def update(self):
            self.rect.y -= self.speedy
        #   if self.rect.centery == HEIGHT/2:
            if self.rect.centery == 50:
               self.kill()

    class Bomb(pygame.sprite.Sprite):

        def __init__(self, t, u):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 20))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
        #    print('inside class' + str(self.rect.x))
            self.rect.centerx = t
            self.rect.centery = u
            self.speedy = +10
            self.shield = 3
            self.back = 0

        def update(self):

            ##stop bomb from falling off plane
            if self.rect.centery > 146:
                self.rect.y += self.speedy


        #    set bomb to move inline with plane with key movemen
            if self.rect.y == 136:
                #print('< 154')
                self.speedx = 0
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_LEFT]:
                #    print('left' + str(self.rect.x))
                    self.rect.x -= 5
                #    print('left2' + str(self.rect.x))
                if keystate[pygame.K_RIGHT]:
                    self.rect.x += 5

         #   this needs alteringmove bomb inline with plane
        #    stops bomb going off screen
            pr = WIDTH - 60
            if self.rect.right > pr:
                self.rect.right = pr

        #    stops bomb going off screen
            pl = 59
            if self.rect.left < pl:
                self.rect.left = pl

            ##stops bomb going off screen
        #    pr = WIDTH - 100
        #    if self.rect.right > pr:
        #        self.rect.right = pr



    class Target(pygame.sprite.Sprite):

        def __init__(self, x, y, color, t_name):
            # this line is required to properly create the sprite
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((80, 80))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.shield = 3
            self.name = t_name


    # Setup - initalise pygame and its objects
    #def go():
    #sprites
    planes = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
        #static = pygame.sprite.Group()
    missiles = pygame.sprite.Group()

        #create a player
    plane = Plane()
    bomb_static = Bomb(plane.rect.centerx, plane.rect.centery + 60)
        #bomb_static = Bomb(50,145)    print('init' + str(bomb_static.rect.y))

        #create a Mob
    tar1 = Target(100, 550, RED, 'red')
    tar2 = Target(300, 550, GREEN, 'green')
    tar3 = Target(500, 550, BLUE, 'blue')

        #create the missiles
    missile1 = Missile(tar1.rect.x, tar1.rect.top)
    missile2 = Missile(tar2.rect.x, tar2.rect.top)
    missile3 = Missile(tar3.rect.x, tar3.rect.top)

        #add missiles to targets
    missiles.add(missile1)
    missiles.add(missile2)
    missiles.add(missile3)

        #add to sprite group
    planes.add(plane)
    bombs.add(bomb_static)

        #all_sprites.add(bomb)

    targets.add(tar1)
    targets.add(tar2)
    targets.add(tar3)

        #load sounds
    bomb_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
    hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
    game_sound = pygame.mixer.music.load(os.path.join(snd_dir, 'game.ogg'))
    pygame.mixer.music.set_volume(0.4)

        #Game Loop
        #pygame.mixer.music.play(loops=-1)
    delay = 2000

        ##start inital missile
    CATONKEYBOARD = pygame.USEREVENT + 1
        ##call/push event after 2000ms
    pygame.time.set_timer(CATONKEYBOARD, 2000)

    endgame = ''
    time_r = ''

    start_ticks=pygame.time.get_ticks()

    while running:

            ##push alert to queue
            ##start repeated missile
            CATONKEYBOARD = pygame.USEREVENT + 1
        #    print('xxxxxx' + str(bomb_static.rect.y))

            ##catch above alert
            if pygame.event.get(CATONKEYBOARD):
                #create the missiles
                missile1 = Missile(tar1.rect.x, tar1.rect.top)
                missile2 = Missile(tar2.rect.x, tar2.rect.top)
                missile3 = Missile(tar3.rect.x, tar3.rect.top)

                #add missiles to targets
                missiles.add(missile1)
                missiles.add(missile2)
                missiles.add(missile3)

                # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bomb = Bomb(plane.rect.centerx, plane.rect.centery + 60)
                        bomb.rect.centery += 10
                        bomb_sound.play()
                        bombs.add(bomb)
                    if event.key == pygame.K_ESCAPE:
                        #exit()
                        return

            ## Process input (has a user event happened , <- , -> , [space] )
            #for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            ## create bomb and drop it when space is pressed
                #elif event.type == pygame.KEYDOWN:

            ##check whether bomb hit target
            collidedict = pygame.sprite.groupcollide(bombs, targets, True, False)

            ##check whether missile hit plane
            collidedict1 = pygame.sprite.groupcollide(missiles, planes, False, False)

            ##remove plane if missile hits plane
            if collidedict1:
                for value1 in collidedict1.values():
                    for currentSprite1 in value1:
                        currentSprite1.shield -= 1

                        shield1 = currentSprite1.shield

                        if shield1 <= 0:
                            #get the score
                        #    getScore()
                            planes.remove(currentSprite1)
                            if bool(planes) == False:
                                time_r = seconds=((pygame.time.get_ticks()-start_ticks) / 1000)
                                writescore(time_r)
                                endgame = getScore()


            ##remove target if missile hits target
            if collidedict:
                for value in collidedict.values():
                    #print(value)
                    for currentSprite in value:
                        #ntargets.remove(currentSprite)
                        #print(currentSprite)
                        currentSprite.shield -= 1
                        shield = currentSprite.shield
                        shield_name = currentSprite.name

                        if shield <= 0:
                            targets.remove(currentSprite)
                            shield_name = ''
                            shield = 3

            #Update method - moves sprites
            planes.update()
            bombs.update()
            targets.update()
            missiles.update()

            #Draw

            screen.fill(BLACK)
            planes.draw(screen)
            targets.draw(screen)
            bombs.draw(screen)
            missiles.draw(screen)

            #draw_text(screen, 'your score' + ' ' + str(score), 18, WIDTH/2, 10)
            draw_text(screen, 'shield' + ' ' + str(shield), 18, WIDTH/2, 50)
            draw_text(screen, 'shield name' + ' ' + str(shield_name), 18, 280, 50)
            draw_text(screen, 'Your score' + '' + str(time_r), 18, 280, 100)

            # after drawing everything
            pygame.display.flip()
