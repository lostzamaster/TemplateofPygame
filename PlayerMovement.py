import pygame as pg
import random
import os

WIDTH = 980 # Screen width
HEIGHT = 680 # Screen HeightWS
FPS = 60 # Fps to run

#RGB Color value
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKYBLUE = (66,203,245)
ORANGE = (245,144,66)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Sprite')
pg.init() # Start
pg.mixer.init() # Sound Start
screen = pg.display.set_mode((WIDTH,HEIGHT))#Seting Scene
player_img = pg.image.load(os.path.join(img_folder , 'p1_jump.png')).convert()#Calling Sprite
pg.display.set_caption("My Game")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.transform.flip(player_img , True , False)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2 , HEIGHT/2  
        self.y_direction = 5
        self.OnRight = True
    def update(self):
        self.rect.y += self.y_direction
        if self.OnRight == True and self.rect.right > WIDTH:
            self.OnRight = False
        elif self.OnRight == False and self.rect.left < 0:
            self.OnRight = True

        if self.OnRight == True:
            self.rect.x += 5
            self.image = player_img
        elif self.OnRight == False:
            self.rect.x -= 5
            self.image = pg.transform.flip(player_img , True , False)

        if self.rect.top < 100:
            self.y_direction = 5
        elif self.rect.bottom > HEIGHT-100:
            self.y_direction = -5        

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

running = True

while running:
    clock.tick(FPS)
    #Input
    for event in pg.event.get():
        #Check Closing
        if event.type == pg.QUIT:
            running = False
    #Update
    all_sprites.update()
    #Drawing
    screen.fill(SKYBLUE)
    all_sprites.draw(screen)
    #EndofDrawing
    pg.display.flip()

pg.quit()