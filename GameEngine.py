
class GameEngine:
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.whitesTurn = True
        self.moveLog = []

    def getLegalMoves(self, piece):
        legalMoves = []
        if piece == 'br' or piece == 'wr':
            legalMoves = rookLegalMoves()

    def makeMove(self, move):
        From = move[0]
        To = move[1]
        pieceMoved = self.board[From[0]][From[1]]
        chessNotation = self.getChessNotation(From, To)
        print(chessNotation)
        if pieceMoved != '--':
            self.board[From[0]][From[1]] = '--'
            self.board[To[0]][To[1]] = pieceMoved
            self.moveLog.append(chessNotation)
            self.whitesTurn = not self.whitesTurn

    def getChessNotation(self, From, To):
        intToFile = {
            0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'
        }
        intToRank = {
            7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'
        }
        return intToFile[From[1]] + intToRank[From[0]] + intToFile[To[1]] + intToRank[To[0]]

    def rookLegalMoves():
