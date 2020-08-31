
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

    def getAllLegalMoves(self):

        legalMoves = []
        # for r in range(8):
        #     for c in range(8):
        #         turn = self.board[r][c][0]
        #         if (turn == 'w' and self.whitesTurn) or (turn == 'b' and not self.whitesTurn):
        #             piece = self.board[r][c][1]
        #         if piece == 'p':
        #             self.getPawnMoves(r, c)
        # turn = self.board[r][c][0]

        for row in range(8):
            for col in range(8):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whitesTurn) or (turn == 'b' and not self.whitesTurn):
                    piece = self.board[row][col][1]
                    if piece == 'p':  # pawn
                        self.getPawnMoves(row, col, legalMoves)
                    elif piece == 'r':  # rook
                        self.getRookMoves(row, col, legalMoves)
                    elif piece == 'b':  # bishop
                        self.getBishopMoves(row, col, legalMoves)
                    elif piece == 'q':
                        self.getBishopMoves(row, col, legalMoves)
                        self.getRookMoves(row, col, legalMoves)
                    elif piece == 'k':
                        self.getKingMoves(row, col, legalMoves)
                    elif piece == 'n':
                        self.getKnightMoves(row, col, legalMoves)
        print(legalMoves)
        return legalMoves

    def getPawnMoves(self, r, c, moves):
        # white
        if self.board[r][c][0] == 'w' and self.whitesTurn:
            if r-1 >= 0:
                if self.board[r-1][c] == '--':
                    moves.append(self.getChessNotation((r, c), (r-1, c)))
            if r == 6 and self.board[r-2][c] == '--':
                moves.append(self.getChessNotation((r, c), (r-2, c)))
            if r-1 >= 0 and c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(
                        self.getChessNotation((r, c), (r-1, c+1)))
            if r-1 >= 0 and c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(
                        self.getChessNotation((r, c), (r-1, c-1)))
        # black
        elif self.board[r][c][0] == 'b' and not self.whitesTurn:
            if r+1 <= 7:
                if self.board[r+1][c] == '--':
                    moves.append(self.getChessNotation((r, c), (r+1, c)))
            if r == 1 and self.board[r+2][c] == '--':
                moves.append(self.getChessNotation((r, c), (r+2, c)))
            if r+1 <= 7 and c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(
                        self.getChessNotation((r, c), (r+1, c+1)))
            if r+1 <= 7 and c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(
                        self.getChessNotation((r, c), (r+1, c-1)))

    def getRookMoves(self, r, c, moves):
        enemyColor = 'b' if self.whitesTurn else 'w'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8, 1):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    endPiece = self.board[row][col]
                    if endPiece == '--':
                        moves.append(
                            self.getChessNotation((r, c), (row, col)))
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            self.getChessNotation((r, c), (row, col)))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        enemyColor = 'b' if self.whitesTurn else 'w'
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        for d in directions:
            for i in range(1, 8, 1):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    endPiece = self.board[row][col]
                    if endPiece == '--':
                        moves.append(
                            self.getChessNotation((r, c), (row, col)))
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            self.getChessNotation((r, c), (row, col)))
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        allyColor = 'w' if self.whitesTurn else 'b'
        knightMoves = (
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1)
        )
        for km in knightMoves:
            row = r + km[0]
            col = c + km[1]
            if 0 <= row < 8 and 0 <= col < 8:
                endPiece = self.board[row][col]
                if endPiece[0] != allyColor:
                    moves.append(self.getChessNotation((r, c), (row, col)))

    def getKingMoves(self, r, c, moves):
        allyColor = 'w' if self.whitesTurn else 'b'
        directions = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1)
        )
        for i in range(8):
            row = r + directions[i][0]
            col = c + directions[i][1]
            if 0 <= row < 8 and 0 <= col < 8:
                endPiece = self.board[row][col]
                if endPiece[0] != allyColor:
                    moves.append(self.getChessNotation((r, c), (row, col)))
