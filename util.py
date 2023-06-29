def is_legal(board, spot, num):
    x, y = spot

    # Check columns
    for i in range(len(board)):
        if board[x][i]["num"] == num:
            return False

    # Check rows
    for i in range(len(board)):
        if board[i][y]["num"] == num:
            return False

    # Check square

    return True
