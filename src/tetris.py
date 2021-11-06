import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# i-block = cyan
# j-block = blue
# l-block = orange
# o-block = yellow
# s-block = green
# t-block = purple
# z-block = red

colours = [
    (0, 255, 255),  # i-block
    (0, 0, 255),  # j-block
    (255, 128, 0),  # l-block
    (255, 255, 0),  # o-block
    (0, 255, 0),  # s-block
    (255, 0, 255),  # t-block
    (255, 0, 0)  # z-block
]


class Piece:
    # coordinates of piece
    x = 0
    y = 0

    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],  # i-block
        [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 8, 9]],  # j-block
        [[2, 4, 5, 6], [1, 5, 9, 10], [4, 5, 6, 8], [0, 1, 5, 9]],  # l-block
        [[1, 2, 5, 6]],  # o-block
        [[1, 2, 4, 5], [0, 4, 5, 9]],  # s-block
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],  # t-block
        [[0, 1, 5, 6], [1, 4, 5, 8]]  # z-block
    ]

    def __init__(self, x, y):
        self.x = x  # initial x coord (from top left)
        self.y = y  # initial y coord (from top left)
        self.type = random.randint(1, len(self.figures))
        self.colour = colours[self.type - 1]
        self.rotation = 0

    def image(self):
        return self.figures[self.type - 1][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type - 1])


class Tetris:
    level = 2  # contributes to speed
    score = 0
    state = "start"  # state of play
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    piece = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []  # 2D array to represent board
        self.score = 0
        self.state = "start"  # state of play
        # fill board with 0s
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_piece(self):
        self.piece = Piece(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in self.piece.image():
                    if (i + self.piece.y > self.height - 1) or \
                            (j + self.piece.x > self.width - 1) or \
                            (j + self.piece.x < 0) or \
                            (self.field[i + self.piece.y][j + self.piece.x] > 0):
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_down(self):
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            self.freeze()

    def go_space(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in self.piece.image():
                    self.field[i + self.piece.y][j + self.piece.x] = self.piece.type
        self.break_lines()
        self.new_piece()
        if self.intersects():
            self.state = "gameover"
        # self.print_field()

    def go_side(self, dx):
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def rotate(self):
        old_rotation = self.piece.rotation
        self.piece.rotate()
        if self.intersects():
            self.piece.rotation = old_rotation

    def print_field(self):
        print("NEW FIELD")
        for row in self.field:
            for val in row:
                print(str(val) + "\t", end="")
            print()


# initialise game engine
pygame.init()

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
SIZE = (500, 600)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tetris")

running = True
clock = pygame.time.Clock()
fps = 10
game = Tetris(20, 10)
counter = 0
pressing_down = False

pygame.mixer.music.load("../music/tetris-gameboy-02.mp3")
pygame.mixer.music.play(loops=-1)
while running:
    if game.piece is None:
        game.new_piece()
    counter += 1
    if counter > 1000:
        counter = 0

    if ((counter % (fps // game.level // 2) == 0) or pressing_down) and \
            (game.state == "start"):
        game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()  # immediately go to bottom
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_DOWN:
                pressing_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(
                surface=screen, color=GRAY,
                rect=[game.x + game.zoom * j,
                      game.y + game.zoom * i,
                      game.zoom - 2, game.zoom - 1], width=1
            )
            if game.field[i][j] > 0:
                pygame.draw.rect(
                    screen, colours[game.field[i][j] - 1],
                    [game.x + game.zoom * j + 1,
                     game.y + game.zoom * i + 1,
                     game.zoom - 2, game.zoom - 2]
                )

    if game.piece is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j  # position
                if p in game.piece.image():
                    pygame.draw.rect(
                        screen, game.piece.colour,
                        [game.x + game.zoom * (j + game.piece.x) + 1,
                         game.y + game.zoom * (i + game.piece.y) + 1,
                         game.zoom - 2, game.zoom - 2]
                    )

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    score_text = font.render("Score: " + str(game.score), True, WHITE)
    level_text = font.render("Level: " + str(game.level), True, WHITE)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(score_text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
