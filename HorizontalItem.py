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
    
bullet_img = pg.image.load(path.join(img_dir , 'Blast.png')).convert()
player_img = pg.image.load(path.join(img_dir , "Ship.png")).convert()
player_mini_img = pg.transform.scale(player_img , (30 , 18))
player_mini_img.set_colorkey(WHITE)
mobs_img = []
mobs_img_list = ['ufoBlue.png','ufoGreen.png','ufoRed.png','ufoYellow.png']
for img in mobs_img_list:
    appendmobs = pg.image.load(path.join(img_dir, img)).convert()
    randomScale = random.randrange(10 ,120)
    appendmobsScaled = pg.transform.scale(appendmobs , (randomScale,randomScale))
    mobs_img.append(appendmobsScaled)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img , (100 , 100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img , (90 , 90))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_image = {}
powerup_image['hp'] = pg.image.load(path.join(img_dir,'powerupGreen_shield.png')).convert()
powerup_image['gun'] = pg.image.load(path.join(img_dir,'powerupRed_bolt.png')).convert()
#Import Sound
shoot_sound = pg.mixer.Sound(path.join(snd_dir,'weaponfire4.wav'))
shoot_sound.set_volume(0.4)

death_sound = pg.mixer.Sound(path.join(snd_dir ,'antimaterhit.wav'))

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
        self.hp = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()
    def update(self):
        self.speedY = 0
        keystate = pg.key.get_pressed()
        if  keystate[pg.K_UP]:
            self.speedY = -8
        if keystate[pg.K_DOWN]:
            self.speedY = 8 
        if keystate[pg.K_SPACE]:
            self.shoot()

        self.rect.y += self.speedY    

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centery = HEIGHT / 2
            self.rect.left = 10
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > 10000:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.right , self.rect.centery)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.centerx , self.rect.top)
                bullet2 = Bullet(self.rect.centerx , self.rect.bottom)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (-500 , HEIGHT / 2)
    
    def powerup(self):
        self.power += 1
        if self.power >= 3:
            self.power = 2
        self.power_time = pg.time.get_ticks()

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
        if self.rect.left < -70:
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

class Explosion(pg.sprite.Sprite):
    def __init__(self , center , size):
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(explosion_anim[self.size]):
                self.kill()    
        else:
            center = self.rect.center
            self.image = explosion_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

class PowerUp(pg.sprite.Sprite):
    def __init__(self , center , y):
        super().__init__()
        self.type = random.choice(['hp' , 'gun'])
        self.image = powerup_image[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -2
        self.speedy = y
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if  self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy *= -1   
        
        if self.rect.left < -10:
            self.kill

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
player = Player()
bullets = pg.sprite.Group()
powerups = pg.sprite.Group()
all_sprites.add(player)

def NewMob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(10):
    NewMob()

score = 0 

font_name = pg.font.match_font('arial')
def draw_text(surf , text , size , x , y):
    font = pg.font.Font(font_name , size)
    text_surface = font.render(text , True , WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface , text_rect)

def draw_hp_bar(surf , x ,y , hp):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 400
    BAR_HIGHT = 20
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x , y , BAR_LENGTH , BAR_HIGHT)
    fill_rect = pg.Rect(x , y , fill , BAR_HIGHT)
    pg.draw.rect(surf , RED , fill_rect)
    pg.draw.rect(surf , WHITE , outline_rect , 2)

def draw_live(surf , x , y , lives , img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img , img_rect)

pg.mixer.music.play(loops=-1)
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

    hits = pg.sprite.groupcollide(mobs , bullets , True , True)
    for hit in hits:
        score += 60 - hit.radius
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center , 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = PowerUp(hit.rect.center , random.randrange(-3 , 3))
            all_sprites.add(pow)
            powerups.add(pow)
        NewMob()
    
    hits = pg.sprite.spritecollide(player , powerups , True)
    for hit in hits:
        if hit.type == 'hp':
            player.hp += random.randrange(10 , 30)
            if player.hp >= 100:
                player.hp = 100
        if hit.type == 'gun':
            player.powerup() 

    hits = pg.sprite.spritecollide(player,mobs,True,pg.sprite.collide_circle)
    for hit in hits:
        player.hp -= hit.radius * 2
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center , 'sm')
        all_sprites.add(expl)
        NewMob()
        if player.hp <= 0:
            death_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.hp = 100  
    if player.lives == 0 and not death_explosion.alive():
        running = False

    #Drawing
    screen.fill(BLACK)
    screen.blit(background , background_rect)
    all_sprites.draw(screen)
    draw_text(screen , str(score) , 30 , 60 , HEIGHT - 50)
    draw_hp_bar(screen , (WIDTH / 2) - 200 , 5 , player.hp)
    draw_live(screen, WIDTH - 100 , 5 , player.lives , player_mini_img)
    #EndofDrawing
    pg.display.flip()
 
pg.quit()
