import chess
ugly_board = [
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']
            ]
board = chess.Board()
board.push_san("e4")
board.push_san("e5")
def drawBoard(screen):
    a = board.fen()
    row = 0
    col = 0
    for i in a:
        if i.isnumeric():
            for j in range(int(i)):
                ugly_board[row][col] = '.'
                col += 1
        elif i.isalpha():
            ugly_board[row][col] = i
            col += 1
        elif i == ' ': # stop parsing, end of FEN
            return 0
        else: # means we reached a '\' and need to go down a row
            row += 1
            col = 0

drawBoard(0)

for i in range(8):
    for j in range(8):
        print(ugly_board[i][j], end=" ")
    print()