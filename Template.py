import pygame as pg
import random

WIDTH = 400 # Screen width
HEIGHT = 300 # Screen HeightWS
FPS = 60 # Fps to run
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pg.init() # Start
pg.mixer.init() # Sound Start
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

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
    #EndofDrawing
    pg.display.flip()

pg.quit()
