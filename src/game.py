import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()  # initialise library

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# define player which extends pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    # move sprite based on user keypresses
    def update(self, pressed_keys, change=5):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -change)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, change)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-change, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(change, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # move sprite based on speed, remove sprite when passed left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# set up drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# creare custom event for adding new enemy
ADDENEMY = pygame.USEREVENT + 1 # events identified in integers, must be unique
pygame.time.set_timer(ADDENEMY, 250)

# instantiate player
player = Player()

# create groups to hold enemy sprites and all sprites
# - enemies used for collision detection + position updates
# - all_sprites used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# setup clock for framerate
clock = pygame.time.Clock()

running = True

# main loop
while running:
    # look at every event in queue
    for event in pygame.event.get():
        # did user hit key?
        if event.type == KEYDOWN:
            # was it escape key?
            if event.key == K_ESCAPE:
                running = False

        # did user click window close button?
        elif event.type == QUIT:
            running = False

        # add a new enemy?
        elif event.type == ADDENEMY:
            # create new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # get set of keys pressed and check for user input, then update player sprite
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()

    # fill screen with white
    screen.fill((0, 0, 0))

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # if so, remove player and stop loop
        player.kill()
        running = False
        print("You collided! GAME OVER!")

    # update display
    pygame.display.flip()

    # ensure program maintains rate of 30 fps
    clock.tick(30)

pygame.quit()
