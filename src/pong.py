import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()  # initialise library

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# variables
x = SCREEN_WIDTH*0.12
y = SCREEN_HEIGHT*0.5
up = K_w
down = K_s
BALL_SPEED_X = -5
BALL_SPEED_Y = 0
SPEED_MOD = 1
P1_SCORE = 0
P2_SCORE = 0
BOUNCE = 0

# define player which extends pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x,y))

    # move sprite based on user keypresses
    def update(self, pressed_keys, change=10):
        if pressed_keys[up]:
            self.rect.move_ip(0, -change)
        if pressed_keys[down]:
            self.rect.move_ip(0, change)
        #if pressed_keys[K_LEFT]:
            #self.rect.move_ip(-change, 0)
        #if pressed_keys[K_RIGHT]:
            #self.rect.move_ip(change, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super(Ball, self).__init__()
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH*0.5,SCREEN_HEIGHT*0.5))
        #self.speed = BALL_SPEED_X

    # move sprite based on speed, remove sprite when passed left edge of screen
    def update(self):
        global BALL_SPEED_Y
        self.rect.move_ip(BALL_SPEED_X*SPEED_MOD, BALL_SPEED_Y *SPEED_MOD)
            #self.kill()
            #running = False
            #print("The Ball has been lost. GAME OVER!")
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            BALL_SPEED_Y = -BALL_SPEED_Y


# set up drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# creare custom event for adding new enemy
ADDBALL = pygame.USEREVENT + 1 # events identified in integers, must be unique
#pygame.time.set_timer(ADDENEMY, 250)

# instantiate players
player1 = Player()
x = SCREEN_WIDTH - SCREEN_WIDTH*0.12
up = K_UP
down = K_DOWN
player2 = Player()

# create groups to hold enemy sprites and all sprites
# - enemies used for collision detection + position updates
# - all_sprites used for rendering
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# add a ball
ball = Ball()
all_sprites.add(ball)

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

        # add a new ball
        #elif event.type == ADDBALL:
            # create new enemy and add it to sprite groups
            #new_enemy = Enemy()
            #enemies.add(new_enemy)
            #all_sprites.add(new_enemy)
            

    # get set of keys pressed and check for user input, then update player sprite
    pressed_keys = pygame.key.get_pressed()
    up = K_w
    down = K_s
    player1.update(pressed_keys)
    up = K_UP
    down = K_DOWN
    player2.update(pressed_keys)

    ball.update()

    # fill screen with white
    screen.fill((0, 0, 0))

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if the ball has collided with either player
    if pygame.sprite.spritecollideany(ball, players):
        
        BALL_SPEED_X = -BALL_SPEED_X
        modY = random.randint(0, 1)
        if (modY == 0):
            modY = -0.1
        else:
            modY = 0.1
        BALL_SPEED_Y = random.randint(20, 50) * modY
        SPEED_MOD += 0.02
        BOUNCE += 1
        if BOUNCE >= 3:
            BOUNCE = 1
        
        # if so, remove player and stop loop
        #player1.kill()
        #running = False
        #print("You collided! GAME OVER!")

    # ball is out of bounds
    if ball.rect.right < 0 or ball.rect.left > SCREEN_WIDTH:
        
        ball.kill()
        pygame.time.delay(1000)
        ball = Ball()
        all_sprites.add(ball)
        BALL_SPEED_X = -5
        BALL_SPEED_Y = 0
        SPEED_MOD = 1
        
        if BOUNCE != 0:
            if BOUNCE == 1:
                P1_SCORE += 1
            else:
                P2_SCORE += 1
            BOUNCE = 0
    
    if (P1_SCORE >= 11):
        running = False
        print("PLAYER 1 WINS! GAME OVER!")
    if (P2_SCORE >= 11):
        running = False
        print("PLAYER 2 WINS! GAME OVER!")
    
    font = pygame.font.SysFont('Calibri', 25, True, False)
    p1_score = font.render(str(P1_SCORE), True, WHITE)
    screen.blit(p1_score, [SCREEN_WIDTH*0.1,0])
    p2_score = font.render(str(P2_SCORE), True, WHITE)
    screen.blit(p2_score, [SCREEN_WIDTH-SCREEN_WIDTH*0.1,0])
    
    # update display
    pygame.display.flip()

    # ensure program maintains rate of 30 fps
    clock.tick(30)

pygame.quit()
