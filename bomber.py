# Import pygame and libraries
import random
from random import randrange
import time
import datetime
import os
import pygame
import eztext

from pygame.locals import *
from score import getScore
from score import writescore
from db import Post



# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# -----------------------------------------------------------------------------
# Constants and global variables
#ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
#         'Author: {0}'.format(pygameMenu.__author__),
#         PYGAMEMENU_TEXT_NEWLINE,
#         'Email: {0}'.format(pygameMenu.__email__)]
#COLOR_BLUE = (12, 12, 200)
#COLOR_BACKGROUND = [128, 0, 128]
#COLOR_WHITE = (255, 255, 255)
#FPS = 60
#H_SIZE = 600  # Height of window size
#HELP = ['Press ESC to enable/disable Menu',#
#        'Press ENTER to access a Sub-Menu or use an option',#
#        'Press UP/DOWN to move through Menu',
#        'Press LEFT/RIGHT to move through Selectors']
#SCORES = ['100','200']
#W_SIZE = 800  # Width of window size


# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
#for m in HELP:
#    print(m)

# Create window
#surface = pygame.display.set_mode((W_SIZE, H_SIZE))
#pygame.display.set_caption('PygameMenu example')

# Main timer and game clock
#clock = pygame.time.Clock()
#timer = [0.0]
#dt = 1.0 / FPS
#timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)


# -----------------------------------------------------------------------------

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

#running = True
#create python class


shield_name = ''

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
        if self.rect.centery == 50:
           self.kill()

class JDAM(pygame.sprite.Sprite):

    def __init__(self, t, u):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = t
        self.rect.centery = u
        self.speedy = +10
        shield = 3
        self.back = 0

    def update(self):

        ##stop JDAM from falling off plane
        if self.rect.centery > 146:
            self.rect.y += self.speedy

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

        pr = WIDTH - 60
        if self.rect.right > pr:
            self.rect.right = pr

        pl = 59
        if self.rect.left < pl:
            self.rect.left = pl

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

class main_game():

    def __init__(self):

        CATONKEYBOARD = pygame.USEREVENT + 1
                ##call/push event after 2000ms
        pygame.time.set_timer(CATONKEYBOARD, 2000)

        self.endgame = ''

        self.start_ticks = pygame.time.get_ticks()
        #sprites
        self.planes = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
            #static = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()

        #create a player
        self.plane = Plane()
        self.bomb_static = JDAM(self.plane.rect.centerx, self.plane.rect.centery + 60)
            #bomb_static = Bomb(50,145)    print('init' + str(bomb_static.rect.y))

            #create a Mob
        self.tar1 = Target(100, 550, RED, 'red')
        self.tar2 = Target(300, 550, GREEN, 'green')
        self.tar3 = Target(500, 550, BLUE, 'blue')

            #create the self.missiles
        self.missile1 = Missile(self.tar1.rect.x, self.tar1.rect.top)
        self.missile2 = Missile(self.tar2.rect.x, self.tar2.rect.top)
        self.missile3 = Missile(self.tar3.rect.x, self.tar3.rect.top)

            #add self.missiles to self.targets
        self.missiles.add(self.missile1)
        self.missiles.add(self.missile2)
        self.missiles.add(self.missile3)

            #add to sprite group
        self.planes.add(self.plane)
        self.bombs.add(self.bomb_static)

            #all_sprites.add(bomb)

        self.targets.add(self.tar1)
        self.targets.add(self.tar2)
        self.targets.add(self.tar3)

            #load sounds
        self.bomb_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
        self.game_sound = pygame.mixer.music.load(os.path.join(snd_dir, 'game.ogg'))
        pygame.mixer.music.set_volume(0.4)

        self.delay = 2000

        self.time_r = ''

        self.shield_name = ''

        self.shield = 3

        self.running = True

    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


    def boomb(self):
            CATONKEYBOARD = pygame.USEREVENT + 1

            if pygame.event.get(CATONKEYBOARD):
                #create the self.self.missiles
                self.missile1 = Missile(self.tar1.rect.x, self.tar1.rect.top)
                self.missile2 = Missile(self.tar2.rect.x, self.tar2.rect.top)
                self.missile3 = Missile(self.tar3.rect.x, self.tar3.rect.top)

                #add self.missiles to self.targets
                self.missiles.add(self.missile1)
                self.missiles.add(self.missile2)
                self.missiles.add(self.missile3)

                # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bomb = JDAM(self.plane.rect.centerx, self.plane.rect.centery + 60)
                        self.bomb.rect.centery += 10
                        self.bomb_sound.play()
                        self.bombs.add(self.bomb)

                    if event.key == pygame.K_ESCAPE:
                        print('escape')
                        self.running = False

            #for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def collide(self):

            collidedict = pygame.sprite.groupcollide(self.bombs, self.targets, True, False)
            collidedict1 = pygame.sprite.groupcollide(self.missiles,self.planes, False, False)

            if collidedict1:
                for value1 in collidedict1.values():
                    for currentSprite1 in value1:
                        print(currentSprite1)
                        currentSprite1.shield -= 1
                        shield1 = currentSprite1.shield

                        if shield1 <= 0:
                            self.planes.remove(currentSprite1)
                            self.bombs.remove(self.bomb_static)

                            if bool(self.planes) == False:
                                self.time_r = seconds=((pygame.time.get_ticks() - self.start_ticks) / 1000)

                                score_1 = Post(
                                    name='player1',
                                    score=self.time_r
                                )
                                score_1.save()       # This will perform an insert
                                print(score_1.score)
                    #            return score_1
                                #writescore(self.time_r)
                                #endgame = getScore()
                                self.running = False

            ##remove target if missile hits target
            if collidedict:
                for value in collidedict.values():
                    #print(value)
                    for currentSprite in value:
                        currentSprite.shield -= 1
                        shield = currentSprite.shield
                        self.shield_name = currentSprite.name

                        if shield <= 0:
                            self.targets.remove(currentSprite)
                            shield_name = ''
                            shield = 3
    def move(self):
            self.planes.update()
            self.bombs.update()
            self.targets.update()
            self.missiles.update()

    def display_refresh(self):
            screen.fill(BLACK)
            self.planes.draw(screen)
            self.targets.draw(screen)
            self.bombs.draw(screen)
            self.missiles.draw(screen)

            #draw_text(screen, 'your score' + ' ' + str(score), 18, WIDTH/2, 10)
            self.draw_text(screen, 'shield' + ' ' + str(shield), 18, WIDTH/2, 50)
            self.draw_text(screen, 'shield name' + ' ' + str(self.shield_name), 18, 280, 50)
            self.draw_text(screen, 'Your score' + '' + str(self.time_r), 18, 280, 100)

            # after drawing everything
            pygame.display.flip()

    def main_loop(self):

            txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='Vhat is Vour Nam: ')

            if not self.running:
                print('enable')
                menu.enable()
            else:
                while self.running:

                        # events for txtbx
                        events = pygame.event.get()
                        # process other events
                        for event in events:
                            # close it x button si pressed
                            if event.type == QUIT: return

                            elif event.type == KEYDOWN:
                                if event.key == pygame.K_RETURN:
        #create game loop                            print('return')
                                    self.boomb()
                                    self.collide()
                                    self.move()
                                #    self.display_refresh()
                        # clear the screen
                        screen.fill((255,255,255))
                        # update txtbx
                        txtbx.update(events)
                        # blit txtbx on the sceen
                        txtbx.draw(screen)
                        # refresh the display
                        pygame.display.flip()



#test local startup
#start = main_game()
#start.main_loop()
