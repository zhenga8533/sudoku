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

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        self.board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Remove some nums
        squares = side * side
        empties = squares * 3 // 4
        for p in sample(range(squares), empties):
            self.board[p // side][p % side] = 0

        self.draw_ui()

    def play_step(self):
        # 1: collect user input
        legal = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.pos = [pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE]

                # 3: Draw Board
                self.draw_ui()
            elif event.type == KEYDOWN:
                if event.key == K_0:
                    self.board[self.pos[0]][self.pos[1]] = 0
                elif event.key == K_1:
                    self.board[self.pos[0]][self.pos[1]] = 1
                elif event.key == K_2:
                    self.board[self.pos[0]][self.pos[1]] = 2
                elif event.key == K_3:
                    self.board[self.pos[0]][self.pos[1]] = 3
                elif event.key == K_4:
                    self.board[self.pos[0]][self.pos[1]] = 4
                elif event.key == K_5:
                    self.board[self.pos[0]][self.pos[1]] = 5
                elif event.key == K_6:
                    self.board[self.pos[0]][self.pos[1]] = 6
                elif event.key == K_7:
                    self.board[self.pos[0]][self.pos[1]] = 7
                elif event.key == K_8:
                    self.board[self.pos[0]][self.pos[1]] = 8
                elif event.key == K_9:
                    self.board[self.pos[0]][self.pos[1]] = 9
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
                if self.board[i][j]:
                    self.display.blit(font.render(str(self.board[i][j]), False, BLACK),
                                      ((i + 0.2) * BLOCK_SIZE, j * BLOCK_SIZE))

        # Current Block
        rect = pygame.Rect(self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE,
                           BLOCK_SIZE)
        pygame.draw.rect(self.display, RED, rect, 3)

        pygame.display.flip()
