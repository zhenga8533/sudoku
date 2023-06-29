import pygame
from pygame.locals import *
from random import sample

pygame.init()
font = pygame.font.Font('arial.ttf', 75)

# pygame constants
BOARD_SIZE = 9
BLOCK_SIZE = 80

# rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


class sudoku:
    def __init__(self):
        # Pygame display
        self.w = BLOCK_SIZE * BOARD_SIZE
        self.h = BLOCK_SIZE * BOARD_SIZE
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Sudoku')

        self.board = None
        self.pos = [0, 0]
        self.reset()

    def reset(self):
        # Generates Board
        base = 3
        side = base * base

        # pattern for a baseline valid solution
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s):
            return sample(s, len(s))

        base_range = range(base)
        rows = [g * base + r for g in shuffle(base_range) for r in shuffle(base_range)]
        cols = [g * base + c for g in shuffle(base_range) for c in shuffle(base_range)]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        self.board = [[{
            "num": nums[pattern(r, c)],
            "locked": True
        } for c in cols] for r in rows]

        # Remove parts of board
        squares = side * side
        empties = squares * 3 // 4
        for p in sample(range(squares), empties):
            self.board[p // side][p % side] = {
                "num": 0,
                "locked": False
            }

        self.draw_ui()

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
        for i in range(square[0]*3, square[0]*3 + 3):
            for j in range(square[1]*3, square[1]*3 + 3):
                if [i, j] != self.pos and self.board[i][j]["num"] == num:
                    return False

        return True

    def play_step(self):
        # 1: collect user input
        legal = True
        player = self.board[self.pos[0]][self.pos[1]]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.pos = [pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE]
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
                        else:
                            player["num"] = 0
                    elif event.key == K_BACKSPACE:
                        player["num"] = 0
                if event.key == K_UP and self.pos[1] > 0:
                    self.pos[1] -= 1
                elif event.key == K_LEFT and self.pos[0] > 0:
                    self.pos[0] -= 1
                elif event.key == K_DOWN and self.pos[1] < 8:
                    self.pos[1] += 1
                elif event.key == K_RIGHT and self.pos[0] < 8:
                    self.pos[0] += 1
                self.draw_ui()

        return legal

    def draw_ui(self):
        # Draw Board
        self.display.fill(WHITE)
        for i in range(1, BOARD_SIZE):
            thick = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.display, BLACK, (0, i * BLOCK_SIZE), (self.display.get_width(), i * BLOCK_SIZE),
                             thick)
            pygame.draw.line(self.display, BLACK, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, self.display.get_height()),
                             thick)

        # Draw numbers on board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]["num"]:
                    if self.board[i][j]["locked"]:
                        self.display.blit(font.render(str(self.board[i][j]["num"]), False, BLACK),
                                          ((i + 0.2) * BLOCK_SIZE, j * BLOCK_SIZE))
                    else:
                        self.display.blit(font.render(str(self.board[i][j]["num"]), False, GRAY),
                                          ((i + 0.2) * BLOCK_SIZE, j * BLOCK_SIZE))

        # Current Block
        rect = pygame.Rect(self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE,
                           BLOCK_SIZE)
        pygame.draw.rect(self.display, RED, rect, 3)

        pygame.display.flip()
