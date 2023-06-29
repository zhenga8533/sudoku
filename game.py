import pygame


pygame.init()
font = pygame.font.Font('arial.ttf', 75)

# pygame constants
BLOCK_SIZE = 80

# rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


class sudoku:
    def __init__(self):
        # Pygame display
        self.w = BLOCK_SIZE * 9
        self.h = BLOCK_SIZE * 9
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Sudoku')

        self.board = None
        self.current_block = [0, 0]
        self.reset()

    def reset(self):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.draw_ui()

    def play_step(self):
        # 1: collect user input
        legal = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.current_block = [pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE]

                # 3: Draw Board
                self.draw_ui()

        return legal

    def draw_ui(self):
        self.display.fill(WHITE)
        for i in range(1, 9):
            thick = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.display, BLACK, (0, i*BLOCK_SIZE), (self.display.get_width(), i*BLOCK_SIZE), thick)
            pygame.draw.line(self.display, BLACK, (i*BLOCK_SIZE, 0), (i*BLOCK_SIZE, self.display.get_height()), thick)

        # self.display.blit(font.render(self.board[i][j], False, BLUE), ((i+0.1)*BLOCK_SIZE, j*BLOCK_SIZE))

        # Current Block
        rect = pygame.Rect(self.current_block[0]*BLOCK_SIZE, self.current_block[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.display, RED, rect, 3)

        pygame.display.flip()