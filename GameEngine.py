import chess

real_board = chess.Board()

##
# Fix chess notation so instead of g1f3 it needs to say Nf3 . . .
##


class GameEngine():
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.whiteTurn = True
        self.moveLog = []

    def get_legal_moves(self, piece):
        pass

    def make_move(self, move, ext_board):
        if move.pieceMoved != '.':
            try:
                # real_move = chess.Move.from_uci(move.getChessNotation())
                print(move.getChessNotation(ext_board))
                real_board.push_san(move.getChessNotation(ext_board))
                self.board[move.startRow][move.startCol] = '.'
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)
                self.whiteTurn = not self.whiteTurn
            # print(real_board)
            except:
                print("error")
            # print(real_board)


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

    def getChessNotation(self, board):
        piece = ''
        if board[self.startRow][self.startCol] == 'br' or board[self.startRow][self.startCol] == 'wr':
            piece = 'R'
        if board[self.startRow][self.startCol] == 'bb' or board[self.startRow][self.startCol] == 'wb':
            piece = 'B'
        if board[self.startRow][self.startCol] == 'bn' or board[self.startRow][self.startCol] == 'wn':
            piece = 'N'
        if board[self.startRow][self.startCol] == 'bk' or board[self.startRow][self.startCol] == 'wk':
            piece = 'K'
        if board[self.startRow][self.startCol] == 'bq' or board[self.startRow][self.startCol] == 'wq':
            piece = 'Q'
        if board[self.startRow][self.startCol] == 'bp' or board[self.startRow][self.startCol] == 'wp':
            piece = self.getRankFile(self.startRow, self.startCol)

        return piece + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
