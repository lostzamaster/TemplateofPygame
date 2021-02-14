import pygame as pg
import random

WIDTH = 980 # Screen width
HEIGHT = 680 # Screen HeightWS
FPS = 60 # Fps to run
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKYBLUE = (66,203,245)
ORANGE = (245,144,66)

pg.init() # Start
pg.mixer.init() # Sound Start
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50 , 50))
        self.image.fill(SKYBLUE)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2 , HEIGHT/2  
        self.onright = True
    def update(self):
        if self.onright == True and self.rect.right > WIDTH:
            self.onright = False
        if self.onright == False and self.rect.left < 0:
            self.onright = True
        
        if self.onright == True:
            self.rect.x += 5
        if self.onright == False:
            self.rect.x -= 5

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
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #EndofDrawing
    pg.display.flip()

pg.quit()
