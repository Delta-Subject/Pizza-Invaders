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
pygame.display.set_caption('DEMO | Pizza Invaders v.0.3')
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Folder Config
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, 'assets/')
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
# AUDIO CONFIG

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
        
    def update(self):
        # Movement
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

## Mob Sprite
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 5)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 5)
            self.speedx = random.randrange(-3, 3)

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

player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(10):   # Add n mobs
    mob = Mob()
    mobs.add(mob)
    all_sprites.add(mob)

# Game Loop
active = True
while active:
    CLOCK.tick(FPS)
    # Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:    # Shooting Config
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Updates
    all_sprites.update()

    hit = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_rect_ratio(0.6))
    if hit:
        print('Collision Detected!')

    shooted = pygame.sprite.groupcollide(mobs, bullets, True, True)
    if shooted:
        print('Mob Eliminated')

    # Draws
    WINDOW.fill(GREY)
    WINDOW.blit(bg, bg_rect)
    all_sprites.draw(WINDOW)
    pygame.display.flip() # Run At Last !!

pygame.quit()
