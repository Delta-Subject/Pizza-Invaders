import pygame
import random
import os

# Basic Definitions
WIDTH = 480
HEIGHT = 600
FPS = 60
CHAR_SIZE = (50, 40)
## Colors
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialization
pygame.init()
pygame.mixer.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DEMO | Pizza Invaders v.0.5.1')
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Folder Config
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, 'assets/')
sounds_folder = os.path.join(assets_folder, 'sfx')
# IMG CONFIG
## BackGround
bg_img = pygame.image.load(os.path.join(assets_folder, 'wood 2.jpg'))
bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))   # Mandatory So The BG image has the same size that the window
bg_rect = bg.get_rect()
## Player
player_img = pygame.image.load(os.path.join(assets_folder, 'pizza-1.png'))
player = pygame.transform.scale(player_img, CHAR_SIZE)
player_rect = player.get_rect()
## MOB
mob_img = pygame.image.load(os.path.join(assets_folder, 'meteorBrown_tiny2.png'))
mob = pygame.transform.scale(mob_img, CHAR_SIZE)
mob_rect = mob.get_rect()
## BULLET
bullet_image = pygame.image.load(os.path.join(assets_folder, 'laserBlue06.png'))
bullet = pygame.transform.scale(bullet_image, (10, 20))
bullet_rect = bullet.get_rect()
## Explosions
explosion_animations = {}
explosion_animations['large'] = []
explosion_animations['small'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(assets_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (75, 75))
    explosion_animations['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_animations['small'].append(img_small)

# AUDIO CONFIG
shoot_sound = pygame.mixer.Sound(os.path.join(sounds_folder, 'pew.wav'))
pygame.mixer.music.load(os.path.join(sounds_folder, 'xDeviruchi - Minigame .wav'))
# pygame.mixer.music.set_volume(0.3)        # In case you ever need to low volume
explosion_sounds = []
for sfx in ['expl3.wav', 'expl6.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(sounds_folder, sfx)))

# Sprites Config
## Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        # Movement
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        if score >= 1500:
            self.shoot_delay = 150
            

## Mob Sprite
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = mob_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 5)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 5)
            self.speedx = random.randrange(-3, 3)
        if score > 500:
            self.speedy = random.randrange(4, 7)
        if score > 1000:
            self.speedy = random.randrange(5, 9)
        self.rotate()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

## Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:         # Checks If Bullet Went Offscreen and Kills It
            self.kill()
## Explosion Sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animations[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animations[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animations[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
score = 0
spawned = 0  # 'spawned' variable set to avoid infite mobspawn while score == 500/1000/1500

def new_mob():
    mob = Mob()
    mobs.add(mob)
    all_sprites.add(mob)

for i in range(10):
    new_mob()

# Rendering Functions
font_name = pygame.font.match_font('arial')
def write(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)   # Turned antialising on FALSE
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_bar(surf, x, y, pct, color_1, color_2):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color_1, fill_rect)
    pygame.draw.rect(surf, color_2, outline_rect, 2)

pygame.mixer.music.play(loops=-1)
# Game Loop
active = True
while active:
    CLOCK.tick(FPS)
    # Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    # Updates
    all_sprites.update()

    player_hit = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.6))
    for hit in player_hit:
        player.health -= 10
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        if player.health <= 0:
            print ('Game Over. Total Score: ' + str(score))
            active = False

    mob_hit = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in mob_hit:
        score += 10
        explosion = Explosion(hit.rect.center, 'large')
        all_sprites.add(explosion)
        new_mob()
        random.choice(explosion_sounds).play()
    if score == 500 and spawned == 0:
        for i in range(5):
            new_mob()
        spawned += 1
    if score == 1000 and spawned == 1:
        for i in range(5):
            new_mob()
        spawned += 1
   
    if score == 1500 and spawned == 2:
        for i in range(5):
            new_mob()
        spawned += 1
    # Draws
    WINDOW.fill(GREY)
    WINDOW.blit(bg, bg_rect)
    all_sprites.draw(WINDOW)
    write(WINDOW, str(score), 30, 30, 10)
    draw_bar(WINDOW, 5, HEIGHT - 30, player.health, RED, WHITE)
    pygame.display.flip() # Run At Last !!

pygame.quit()
