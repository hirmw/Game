
import pygame
import random
import os
import time

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
        self.image = pygame.image.load(os.path.join(img_folder, 'plane.xcf')).convert()
        #self.image.fill(GREEN)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.top = 10
        self.speedx = 0

    def update(self):
        # any code here will happen every time the game loop updates

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

    def dropabomb(self):

        bomb = Bomb(self.rect.centerx, self.rect.centery + 50)
        bomb.rect.centery += 10
        bombs.add(bomb)
        bomb_sound.play()
        #bombs.add(bomb)

class Bomb(pygame.sprite.Sprite):

    def __init__(self, t, u):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = t
        self.rect.centery = u
        self.speedy = +10


    def update(self):
            #dropping motion
            #print(self.rect.centery)
        if self.rect.centery > 175:
            #    print('dropped')
            #bombs.add(bomb)
            self.rect.y += self.speedy
            if self.rect.bottom > 800:
                self.kill()

#    def move(self):
        #moving motion
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




class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, color):
            # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 5





    # placehlder for hit method

# Setup - initalise pygame and its objects

#sprites
planes = pygame.sprite.Group()
mods = pygame.sprite.Group()
bombs = pygame.sprite.Group()

#create a player
plane = Plane()
bomb_static = Bomb(plane.rect.centerx, plane.rect.centery + 50 )


#create a Mob
mob1 = Mob(100, 550, RED)
mob2 = Mob(300, 550, GREEN)
mob3 = Mob(500, 550, BLUE)

#add to sprite group
planes.add(plane)
#all_sprites.add(bomb)

mods.add(mob1)
mods.add(mob2)
mods.add(mob3)

#score
score = 0

#load sounds
bomb_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'bomb.wav'))
game_sound = pygame.mixer.music.load(os.path.join(snd_dir, 'game.ogg'))
pygame.mixer.music.set_volume(0.4)

#Game Loop
#pygame.mixer.music.play(loops=-1)



running = True
while running:
    #keep the loop running at the right speed
    clock.tick(fps)


   # Process input (has a user event happened , <- , -> , [space] )
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                plane.dropabomb()

    bombs.add(bomb_static)
  #Update
    planes.update()
    bombs.update()
    mods.update()

    #other sprties movement is in update() but we have modified that to
    # do something else
    #bomb.move()

  #Check for hits (sprite , group)
    #hits = pygame.sprite.groupcollide(bombs, mods, False, False)

    





  #Draw
    screen.fill(BLACK)
    planes.draw(screen)
    mods.draw(screen)
    bombs.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    # after drawing everything
    pygame.display.flip()

pygame.quit()
