import random

import pygame
from pygame.locals import *
from random import sample
from board import tile
import time

# Game Constants
BLOCK_SIZE = 3
BOARD_SIZE = BLOCK_SIZE * BLOCK_SIZE
TILE_SIZE = 30
BLOCKS = [i for i in range(BLOCK_SIZE)]
NUMBERS = [num + 1 for num in range(BOARD_SIZE)]

# RGB Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)


class sudoku:
    def __init__(self, empty):
        # Initialize pygame
        pygame.init()
        self.font = pygame.font.Font('arial.ttf', 25)
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

        # Randomizes board using pattern
        self.board = [[tile(nums[(3 * (row % 3) + row // 3 + col) % 9], True) for col in cols] for row in rows]

        # Remove parts of board
        positions = [[row, col] for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
        for pos in sample(positions, self.empty):
            self.board[pos[0]][pos[1]].reset()

        self.draw_ui()

    def backtrack(self):
        self.board = [[tile(0, False) for row in range(BOARD_SIZE)] for col in range(BOARD_SIZE)]
        self.board[4][4] = tile(random.randint(1, BOARD_SIZE), True)
        self.solve()

    def solve(self):
        # Loop Timeout
        time.sleep(0.99 ** self.empty / 33)
        pos, possible = self.find_lowest()
        if pos == [-1, -1]:
            return True

        # Draw UI
        self.pos = pos[:]
        self.draw_ui()

        # Loop through all numbers
        for num in possible:
            # Try number
            self.board[pos[0]][pos[1]].lock(num)
            self.empty -= 1

            # Check if possible, if not => backtrack
            if self.solve():
                return True
            else:
                self.board[pos[0]][pos[1]].reset()
                self.empty += 1

        return False

    def find_lowest(self) -> object:
        lowest = BOARD_SIZE
        pos = [-1, -1]
        possible = NUMBERS[:]

        for row in sample(range(BOARD_SIZE), BOARD_SIZE):
            for col in sample(range(BOARD_SIZE), BOARD_SIZE):
                if self.board[row][col].num == 0:
                    nums = NUMBERS[:]

                    # Check row
                    for x in range(len(self.board)):
                        num = self.board[row][x].num
                        if num in nums:
                            nums.remove(num)

                    # Check column
                    for y in range(len(self.board)):
                        num = self.board[y][col].num
                        if num in nums:
                            nums.remove(num)

                    # Check square
                    square = [row // 3, col // 3]
                    for y in range(square[0] * 3, square[0] * 3 + 3):
                        for x in range(square[1] * 3, square[1] * 3 + 3):
                            num = self.board[y][x].num
                            if num in nums:
                                nums.remove(num)

                    if len(nums) < lowest:
                        lowest = len(nums)
                        pos = [row, col]
                        possible = nums

        return pos, possible

    def get_possible(self, num, pos):
        # Check row
        for col in range(len(self.board)):
            if num == self.board[pos[0]][col].num and [pos[0], col] != pos:
                return False

        # Check column
        for row in range(len(self.board)):
            if num == self.board[row][pos[1]].num and [row, pos[1]] != pos:
                return False

        # Check square
        square = [pos[0] // 3, pos[1] // 3]
        for row in range(square[0] * 3, square[0] * 3 + 3):
            for col in range(square[1] * 3, square[1] * 3 + 3):
                if num == self.board[row][col].num and [row, col] != pos:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Player mouse position
                pos = pygame.mouse.get_pos()
                self.pos = [pos[0] // TILE_SIZE, pos[1] // TILE_SIZE]
                self.draw_ui()
            elif event.type == KEYDOWN:
                if not player.locked:  # Player number input
                    if event.key == K_0:
                        player.num = 0
                    elif event.key == K_1:
                        player.num = 1
                    elif event.key == K_2:
                        player.num = 2
                    elif event.key == K_3:
                        player.num = 3
                    elif event.key == K_4:
                        player.num = 4
                    elif event.key == K_5:
                        player.num = 5
                    elif event.key == K_6:
                        player.num = 6
                    elif event.key == K_7:
                        player.num = 7
                    elif event.key == K_8:
                        player.num = 8
                    elif event.key == K_9:
                        player.num = 9
                    elif event.key == K_RETURN:
                        if self.get_possible(player.num, self.pos):
                            player.locked = True
                            self.empty -= 1
                        else:
                            player.num = 0
                if event.key == K_UP:  # Control player position
                    self.pos[1] = (self.pos[1] + 8) % 9
                elif event.key == K_LEFT:
                    self.pos[0] = (self.pos[0] + 8) % 9
                elif event.key == K_DOWN:
                    self.pos[1] = (self.pos[1] + 10) % 9
                elif event.key == K_RIGHT:
                    self.pos[0] = (self.pos[0] + 10) % 9
                elif event.key == K_BACKSPACE:  # Delete tile
                    if player.locked:
                        player.num = 0
                        player.locked = False
                        self.empty += 1
                elif event.key == K_SPACE:  # Solve board
                    self.solve()
                self.draw_ui()

                # Control game
                if event.key == K_q:  # Quit
                    pygame.quit()
                    quit()
                elif event.key == K_r:  # Reset
                    game_over = True
                    pygame.quit()

        return game_over

    def draw_ui(self):
        # Draw Board
        self.display.fill(WHITE)
        for i in range(1, BOARD_SIZE + 1):
            thick = 5 if i % BLOCK_SIZE == 0 else 1
            pygame.draw.line(self.display, BLACK, (0, i * TILE_SIZE), (self.display.get_width(), i * TILE_SIZE),
                             thick)
            pygame.draw.line(self.display, BLACK, (i * TILE_SIZE, 0), (i * TILE_SIZE, self.display.get_height()),
                             thick)

        # Draw numbers on board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col].num:
                    color = BLACK if self.board[row][col].locked else GRAY
                    self.display.blit(self.font.render(str(self.board[row][col].num), False, color),
                                      ((row + 0.3) * TILE_SIZE, (col + 0.05) * TILE_SIZE))

        # Current Block
        rect = pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.display, RED, rect, 3)

        # Possible inputs
        for num in range(1, len(self.board) + 1):
            if self.get_possible(num, self.pos):
                self.display.blit(self.font.render(str(num), False, GREEN),
                                  ((num - 0.7) * TILE_SIZE, (len(self.board) + 0.05) * TILE_SIZE))

        # Game complete overlay
        if self.empty == 0:
            font = pygame.font.Font('arial.ttf', 50)
            text = font.render("Congrats!", True, BLUE)
            rect = text.get_rect(center=(self.w / 2, self.h / 2 - TILE_SIZE / 2))

            font = pygame.font.Font('arial.ttf', 20)
            sub_text = font.render("Press r to restart or q to quit.", True, BLUE)
            sub_rect = sub_text.get_rect(center=(self.w / 2, (BOARD_SIZE + 0.5) * TILE_SIZE))
            self.display.blit(text, rect)
            self.display.blit(sub_text, sub_rect)

        pygame.display.flip()
