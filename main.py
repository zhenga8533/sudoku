from game import sudoku


if __name__ == '__main__':
    # Create game
    game = sudoku()

    # game loop
    while True:
        game.play_step()
