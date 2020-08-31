
class GameEngine:
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'wb', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.whitesTurn = True
        self.moveLog = []

    # def getLegalMoves(self, piece):
    #     legalMoves = []
    #     if piece == 'br' or piece == 'wr':
    #         legalMoves = rookLegalMoves()

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

    def getAllLegalMoves(self, square):
        row = square[0]
        col = square[1]
        legalMoves = []
        # for r in range(8):
        #     for c in range(8):
        #         turn = self.board[r][c][0]
        #         if (turn == 'w' and self.whitesTurn) or (turn == 'b' and not self.whitesTurn):
        #             piece = self.board[r][c][1]
        #         if piece == 'p':
        #             self.getPawnMoves(r, c)
        # turn = self.board[r][c][0]
        piece = self.board[row][col][1]
        if piece == 'p':  # pawn
            legalMoves = self.getPawnMoves(row, col)
        elif piece == 'r':  # rook
            legalMoves = self.getRookMoves(row, col)
        elif piece == 'b':  # bishop
            legalMoves = self.getBishopMoves(row, col)
        elif piece == 'q':
            legalMoves = self.getBishopMoves(
                row, col) + self.getRookMoves(row, col)
        elif piece == 'k':
            legalMoves = self.getKingMoves(row, col)
        elif piece == 'n':
            legalMoves = self.getKnightMoves(row, col)
        print(legalMoves)
        return legalMoves

    def getPawnMoves(self, r, c):
        legalMoves = []
        # white
        if self.board[r][c][0] == 'w' and self.whitesTurn:
            if r-1 >= 0:
                if self.board[r-1][c] == '--':
                    legalMoves.append(self.getChessNotation((r, c), (r-1, c)))
            if r == 6 and self.board[r-2][c] == '--':
                legalMoves.append(self.getChessNotation((r, c), (r-2, c)))
            if r-1 >= 0 and c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    legalMoves.append(
                        self.getChessNotation((r, c), (r-1, c+1)))
            if r-1 >= 0 and c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    legalMoves.append(
                        self.getChessNotation((r, c), (r-1, c-1)))
        # black
        elif self.board[r][c][0] == 'b' and not self.whitesTurn:
            if r+1 <= 7:
                if self.board[r+1][c] == '--':
                    legalMoves.append(self.getChessNotation((r, c), (r+1, c)))
            if r == 1 and self.board[r+2][c] == '--':
                legalMoves.append(self.getChessNotation((r, c), (r+2, c)))
            if r+1 <= 7 and c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    legalMoves.append(
                        self.getChessNotation((r, c), (r+1, c+1)))
            if r+1 <= 7 and c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    legalMoves.append(
                        self.getChessNotation((r, c), (r+1, c-1)))
        return legalMoves

    def getRookMoves(self, r, c):
        legalMoves = []
        enemyColor = 'b' if self.whitesTurn else 'w'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8, 1):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    endPiece = self.board[row][col]
                    if endPiece == '--':
                        legalMoves.append(
                            self.getChessNotation((r, c), (row, col)))
                    elif endPiece[0] == enemyColor:
                        legalMoves.append(
                            self.getChessNotation((r, c), (row, col)))
                        break
                    else:
                        break
                else:
                    break
        return legalMoves

    def getBishopMoves(self, r, c):
        legalMoves = []
        enemyColor = 'b' if self.whitesTurn else 'w'
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        for d in directions:
            for i in range(1, 8, 1):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    endPiece = self.board[row][col]
                    if endPiece == '--':
                        legalMoves.append(
                            self.getChessNotation((r, c), (row, col)))
                    elif endPiece[0] == enemyColor:
                        legalMoves.append(
                            self.getChessNotation((r, c), (row, col)))
                    else:
                        break
                else:
                    break
        return legalMoves

    def getKnightMoves(self, r, c):
        pass

    def getKingMoves(self, r, c):
        legalMoves = []
        enemyColor = 'b' if self.whitesTurn else 'w'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            row = r + d[0] * 1
            col = c + d[1] * 1
            if 0 <= row < 8 and 0 <= col < 8:
                endPiece = self.board[row][col]
                if endPiece == '--':
                    legalMoves.append(
                        self.getChessNotation((r, c), (row, col)))
                elif endPiece[0] == enemyColor:
                    legalMoves.append(
                        self.getChessNotation((r, c), (row, col)))
                else:
                    break
            else:
                break
        return legalMoves
