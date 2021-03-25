import pygame as pg
import random
from os import path

WIDTH = 960 # Screen width
HEIGHT = 540 # Screen HeightWS
FPS = 60 # Fps to run

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

img_dir = path.join(path.dirname(__file__), 'Sprite')
snd_dir = path.join(path.dirname(__file__), 'Sound')

pg.init() # Start
pg.mixer.init() # Sound Start
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

#Import Image
background = pg.image.load(path.join(img_dir , 'starfield2.png')).convert()
background_rect = background.get_rect()

player_img = pg.image.load(path.join(img_dir , "Ship.png")).convert()
mobs_img = []
mobs_img_list = ['ufoBlue.png','ufoGreen.png','ufoRed.png','ufoYellow.png']
for img in mobs_img_list:
    appendmobs = pg.image.load(path.join(img_dir, img)).convert()
    randomScale = random.randrange(10 ,120)
    appendmobsScaled = pg.transform.scale(appendmobs , (randomScale,randomScale))
    mobs_img.append(appendmobsScaled)
    
bullet_img = pg.image.load(path.join(img_dir , 'Blast.png')).convert()

#Import Sound
shoot_sound = pg.mixer.Sound(path.join(snd_dir,'weaponfire4.wav'))
shoot_sound.set_volume(0.4)

expl_sound = []
for snd in ['explosion1.wav' , 'explosion2.wav', 'explosion3.wav', 'explosion4.wav']:
    get_sounds = pg.mixer.Sound(path.join(snd_dir , snd))
    get_sounds.set_volume(0.4)
    expl_sound.append(get_sounds)

pg.mixer.music.load(path.join(snd_dir, 'bgm_lungmen_battle_arknights_auMHBXMByoK-gucZe9S9.mp3'))
pg.mixer.music.set_volume(0.4)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img , (50,38))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 19
        #pg.draw.circle(self.image , RED , self.rect.center , self.radius)
        self.rect.centery = HEIGHT / 2
        self.rect.left = 10
        self.speedY = 0
    def update(self):
        self.speedY = 0
        keystate = pg.key.get_pressed()
        if  keystate[pg.K_UP]:
            self.speedY = -8
        if keystate[pg.K_DOWN ]:
            self.speedY = 8 
        self.rect.y += self.speedY    

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mobs_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.height / 2) * 0.85)
        #pg.draw.circle(self.image, RED , self.rect.center , self.radius)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(WIDTH + 40, WIDTH + 100)
        self.speedx = random.randrange(-8 , -1)
        self.speedy = random.randrange(-3 , 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pg.time.get_ticks()
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(WIDTH + 40, WIDTH + 100)
            self.speedx = random.randrange(-8 , -1)
        if  self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy *= -1   
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pg.transform.rotate(self.image_orig , self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(bullet_img , (40,10))
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10
    def update(self):
        self.rect.x += self.speedx
        #Destroy when passed screen
        if self.rect.left > WIDTH:
            self.kill

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
player = Player()
bullets = pg.sprite.Group()
all_sprites.add(player)
for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0 

font_name = pg.font.match_font('arial')
def draw_text(surf , text , size , x , y):
    font = pg.font.Font(font_name , size)
    text_surface = font.render(text , True , WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface , text_rect)

pg.mixer.music.play(loops=-1)
running = True

while running:
    clock.tick(FPS)
    #Input
    for event in pg.event.get():
        #Check Closing
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    #Update
    all_sprites.update()

    hits = pg.sprite.groupcollide(mobs , bullets , True , True)
    for hit in hits:
        score += 60 - hit.radius
        random.choice(expl_sound).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pg.sprite.spritecollide(player,mobs,False,pg.sprite.collide_circle)
    if hits:
        running = False
    #Drawing
    screen.fill(BLACK)
    screen.blit(background , background_rect)
    all_sprites.draw(screen)
    draw_text(screen , str(score) , 30 , 60 , HEIGHT - 50)
    #EndofDrawing
    pg.display.flip()
 
pg.quit()
