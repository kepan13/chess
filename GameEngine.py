import chess

real_board = chess.Board()

##
# Fix chess notation so instead of g1f3 it needs to say Nf3 . . .
##


class GameEngine():
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bk', 'bq', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wk', 'wq', 'wb', 'wn', 'wr']
        ]
        self.whiteTurn = True
        self.moveLog = []

    def get_legal_moves(self, piece):
        pass

    def make_move(self, move):
        if move.pieceMoved != '.':
            try:
                real_move = chess.Move.from_uci(move.getChessNotation())
                real_board.push(real_move)
                self.board[move.startRow][move.startCol] = '.'
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)
                self.whiteTurn = not self.whiteTurn
                print(move.getChessNotation())

                print(real_board)
            except:
                print("error")


class Move():
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
