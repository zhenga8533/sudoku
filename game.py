import pygame
from pygame.locals import *
from random import sample

pygame.init()
font = pygame.font.Font('arial.ttf', 50)

# pygame constants
BLOCK_SIZE = 3
BOARD_SIZE = BLOCK_SIZE * BLOCK_SIZE
TILE_SIZE = 60
BLOCKS = [i for i in range(BLOCK_SIZE)]
NUMBERS = [i + 1 for i in range(BOARD_SIZE)]

# rgb colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


class sudoku:
    def __init__(self, empty):
        # Pygame display
        self.w = TILE_SIZE * BOARD_SIZE
        self.h = TILE_SIZE * (BOARD_SIZE + 1)
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Sudoku')

        self.board = None
        self.empty = empty
        self.pos = [0, 0]
        self.reset()

    def reset(self):
        # Generates board
        rows = [i * BLOCK_SIZE + j for i in sample(BLOCKS, len(BLOCKS))
                for j in sample(BLOCKS, len(BLOCKS))]
        cols = [i * BLOCK_SIZE + j for i in sample(BLOCKS, len(BLOCKS))
                for j in sample(BLOCKS, len(BLOCKS))]
        nums = sample(NUMBERS, len(NUMBERS))

        # Uses randomized baseline pattern
        self.board = [[{
            "num": nums[(3*(row % 3) + row//3 + col) % 9],
            "locked": True
        } for col in cols] for row in rows]

        # Remove parts of board
        positions = [[i, j] for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        for pos in sample(positions, self.empty):
            self.board[pos[0]][pos[1]] = {
                "num": 0,
                "locked": False
            }

        self.draw_ui()

    def solve(self):
        tile = self.board[self.pos[0]][self.pos[1]]
        if not tile["locked"]:
            possible = self.get_possible(self.pos)
            if possible:
                tile["num"] = possible[0]

        # Recursive call
        if self.empty and self.pos != [8, 8]:
            self.pos[1] = (self.pos[1] + 1) % 9
            self.pos[0] += self.pos[1] == 0
            self.solve()

    def get_possible(self, pos):
        possible = NUMBERS[:]

        # Check columns
        for i in range(len(self.board)):
            if i != pos[1] and self.board[pos[0]][i]["num"] in possible:
                possible.remove(self.board[pos[0]][i]["num"])

        # Check rows
        for i in range(len(self.board)):
            if i != pos[0] and self.board[i][pos[1]]["num"] in possible:
                possible.remove(self.board[i][self.pos[1]]["num"])

        # Check square
        square = [pos[0] // 3, pos[1] // 3]
        for i in range(square[0] * 3, square[0] * 3 + 3):
            for j in range(square[1] * 3, square[1] * 3 + 3):
                if [i, j] != pos and self.board[i][j]["num"] in possible:
                    possible.remove(self.board[i][j]["num"])

        return possible

    def check_move(self):
        num = self.board[self.pos[0]][self.pos[1]]["num"]

        # Check columns
        for i in range(len(self.board)):
            if [self.pos[0], i] != self.pos and self.board[self.pos[0]][i]["num"] == num:
                return False

        # Check rows
        for i in range(len(self.board)):
            if [i, self.pos[1]] != self.pos and self.board[i][self.pos[1]]["num"] == num:
                return False

        # Check square
        square = [self.pos[0] // 3, self.pos[1] // 3]
        for i in range(square[0] * 3, square[0] * 3 + 3):
            for j in range(square[1] * 3, square[1] * 3 + 3):
                if [i, j] != self.pos and self.board[i][j]["num"] == num:
                    return False

        return True

    def play_step(self):
        # 1: collect user input
        game_over = False
        player = self.board[self.pos[0]][self.pos[1]]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.pos = [pos[0] // TILE_SIZE, pos[1] // TILE_SIZE]
                self.draw_ui()
            elif event.type == KEYDOWN:
                if not player["locked"]:
                    if event.key == K_0:
                        player["num"] = 0
                    elif event.key == K_1:
                        player["num"] = 1
                    elif event.key == K_2:
                        player["num"] = 2
                    elif event.key == K_3:
                        player["num"] = 3
                    elif event.key == K_4:
                        player["num"] = 4
                    elif event.key == K_5:
                        player["num"] = 5
                    elif event.key == K_6:
                        player["num"] = 6
                    elif event.key == K_7:
                        player["num"] = 7
                    elif event.key == K_8:
                        player["num"] = 8
                    elif event.key == K_9:
                        player["num"] = 9
                    elif event.key == K_RETURN:
                        if self.check_move():
                            player["locked"] = True
                            self.empty -= 1
                        else:
                            player["num"] = 0

                        # Check for complete board
                        if self.empty == 0:
                            game_over = True
                if event.key == K_UP:
                    self.pos[1] = (self.pos[1] + 8) % 9
                elif event.key == K_LEFT:
                    self.pos[0] = (self.pos[0] + 8) % 9
                elif event.key == K_DOWN:
                    self.pos[1] = (self.pos[1] + 10) % 9
                elif event.key == K_RIGHT:
                    self.pos[0] = (self.pos[0] + 10) % 9
                elif event.key == K_BACKSPACE:
                    if player["locked"]:
                        player["num"] = 0
                        player["locked"] = False
                        self.empty += 1
                elif event.key == K_SPACE:
                    self.pos = [0, 0]
                    self.solve()
                self.draw_ui()

        return game_over

    def draw_ui(self):
        # Draw Board
        self.display.fill(WHITE)
        for i in range(1, BOARD_SIZE + 1):
            thick = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.display, BLACK, (0, i * TILE_SIZE), (self.display.get_width(), i * TILE_SIZE),
                             thick)
            pygame.draw.line(self.display, BLACK, (i * TILE_SIZE, 0), (i * TILE_SIZE, self.display.get_height()),
                             thick)

        # Draw numbers on board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]["num"]:
                    if self.board[i][j]["locked"]:
                        self.display.blit(font.render(str(self.board[i][j]["num"]), False, BLACK),
                                          ((i + 0.25) * TILE_SIZE, (j + 0.05) * TILE_SIZE))
                    else:
                        self.display.blit(font.render(str(self.board[i][j]["num"]), False, GRAY),
                                          ((i + 0.25) * TILE_SIZE, (j + 0.05) * TILE_SIZE))

        # Current Block
        rect = pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE,
                           TILE_SIZE)
        pygame.draw.rect(self.display, RED, rect, 3)

        pygame.display.flip()
