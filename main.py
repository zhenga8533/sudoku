from game import sudoku


if __name__ == '__main__':
    while True:
        # Get Game
        while True:
            empty = input('Enter empty tiles [0, 81]: ')
            if empty.isdigit() and 0 <= int(empty) <= 81:
                break
            else:
                print("Please input an integer in [0, 81]")
        game = sudoku(int(empty))

        # Game loop
        while True:
            if game.play_step():
                break
