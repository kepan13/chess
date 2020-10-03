import chess
import pygame
import GameEngine
import os
from random import randrange

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'pieces')



    

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
board = chess.Board()

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

blackRook = pygame.image.load(os.path.join(image_path, 'bR' + '.png'))
blackRook = pygame.transform.scale(blackRook, (SQUARE_SIZE, SQUARE_SIZE))

blackKnight = pygame.image.load(os.path.join(image_path, 'bN' + '.png'))
blackKnight = pygame.transform.scale(blackKnight, (SQUARE_SIZE, SQUARE_SIZE))

blackBishop = pygame.image.load(os.path.join(image_path, 'bB' + '.png'))
blackBishop = pygame.transform.scale(blackBishop, (SQUARE_SIZE, SQUARE_SIZE))

blackQueen = pygame.image.load(os.path.join(image_path, 'bQ' + '.png'))
blackQueen = pygame.transform.scale(blackQueen, (SQUARE_SIZE, SQUARE_SIZE))

blackKing = pygame.image.load(os.path.join(image_path, 'bK' + '.png'))
blackKing = pygame.transform.scale(blackKing, (SQUARE_SIZE, SQUARE_SIZE))

blackPawn = pygame.image.load(os.path.join(image_path, 'bp' + '.png'))
blackPawn = pygame.transform.scale(blackPawn, (SQUARE_SIZE, SQUARE_SIZE))

whiteRook = pygame.image.load(os.path.join(image_path, 'wR' + '.png'))
whiteRook = pygame.transform.scale(whiteRook, (SQUARE_SIZE, SQUARE_SIZE))

whiteKnight = pygame.image.load(os.path.join(image_path, 'wN' + '.png'))
whiteKnight = pygame.transform.scale(whiteKnight, (SQUARE_SIZE, SQUARE_SIZE))

whiteBishop = pygame.image.load(os.path.join(image_path, 'wB' + '.png'))
whiteBishop = pygame.transform.scale(whiteBishop, (SQUARE_SIZE, SQUARE_SIZE))

whiteQueen = pygame.image.load(os.path.join(image_path, 'wQ' + '.png'))
whiteQueen = pygame.transform.scale(whiteQueen, (SQUARE_SIZE, SQUARE_SIZE))

whiteKing = pygame.image.load(os.path.join(image_path, 'wK' + '.png'))
whiteKing = pygame.transform.scale(whiteKing, (SQUARE_SIZE, SQUARE_SIZE))

whitePawn = pygame.image.load(os.path.join(image_path, 'wp' + '.png'))
whitePawn = pygame.transform.scale(whitePawn, (SQUARE_SIZE, SQUARE_SIZE))

def getChessNotation(startSq, endSq):
    intToFile = {0:'a', 1:'b', 2:'c', 3:'d', 4: 'e',
                5: 'f', 6:'g', 7:'h'}
    intToRank = {0: '8',1: '7', 2: '6', 3: '5', 4: '4',
                5: '3', 6: '2', 7: '1'}
    return intToFile[startSq[1]] + intToRank[startSq[0]] + intToFile[endSq[1]] + intToRank[endSq[0]]



def setBoardAfterFEN():
    board_fen = board.fen()
    row = 0
    col = 0
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    for i in board_fen:
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

def print_board(b):
    for i in range(8):
        for j in range(8):
            print(b[i][j], end="")
        print()
    print()

def drawBoard(screen, highlightSq):
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if len(highlightSq):
        row = highlightSq[1]
        col = highlightSq[0]
        highlightColor = (0, 200, 0)
        pygame.draw.rect(screen, highlightColor, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = ugly_board[r][c]
            if piece == 'p':
                screen.blit(blackPawn, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'r':
                screen.blit(blackRook, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'n':
                screen.blit(blackKnight, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'b':
                screen.blit(blackBishop, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'q':
                screen.blit(blackQueen, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'k':
                screen.blit(blackKing, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'P':
                screen.blit(whitePawn, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'R':
                screen.blit(whiteRook, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'N':
                screen.blit(whiteKnight, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'B':
                screen.blit(whiteBishop, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'Q':
                screen.blit(whiteQueen, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif piece == 'K':
                screen.blit(whiteKing, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def updateBoard(screen, highlightSq):
    setBoardAfterFEN()
    drawBoard(screen, highlightSq)
    drawPieces(screen)

def isPromotion(move):
    if move.pieceCaptured != '.':
        return False
    if isWhitesTurn(): # whites turn
        if move.pieceMoved != 'P':
            return False
        if move.startRow == 1 and move.endRow == 0:
            return True
    else: # blacks turn
        if move.pieceMoved != 'p':
            return False
        if move.startRow == 6 and move.endRow == 7:
            return True
    
def isWhitesTurn():
    return board.turn

def getPieceCaptured(chessNotation):
    startFile = chessNotation[0]
    startRank = chessNotation[1]
    endFile = chessNotation[2]
    endRank = chessNotation[3]
    fileToRow = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7 }
    rankToCol = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7 }
    # move = GameEngine.MoveGenerator((fileToRow[startFile], rankToCol[startRank]), (fileToRow[endFile], fileToRow[endRank]), ugly_board)
    # return move.pieceCaptured
    startSq = (fileToRow[startFile], rankToCol[startRank])
    endSq = (fileToRow[endFile], rankToCol[endRank])
    move = GameEngine.MoveGenerator(startSq, endSq, ugly_board)

    return move.pieceCaptured
    
def getPieceValue(move):
    piece = getPieceCaptured(move)
    piece = piece.upper()
    if piece == 'P':
        return 10
    elif piece == 'N':
        return 30
    elif piece == 'B':
        return 30
    elif piece == 'Q':
        return 90
    elif piece == 'R':
        return 50
    else:
        return 0

def minimax():
    moves = []
    moveValue = 0
    bestMove = -9999
    moveIndex = 0

    for move in board.legal_moves:
        moves.append(move)
    for i in range(len(moves)):
        if board.is_capture(moves[i]):
            # print(moves[i])
            moveValue = getPieceValue(str(moves[i]))
            if moveValue >= bestMove:
                bestMove = moveValue
                moveIndex = i
            
            
    if len(moves) == 0:
        print('Check mate!')
        input()
        sys.exit(1)
    

    move = moves[moveIndex]
    board.push(move)
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    selectedSquare = ()
    clicks = []
    moveMade = False
    setBoardAfterFEN()
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    # undo move
                    if len(board.move_stack) > 0:
                        board.pop()
                        print(board)
            elif isWhitesTurn():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    col = x // SQUARE_SIZE
                    row = y // SQUARE_SIZE
                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        clicks = []
                    else:
                        selectedSquare = (row, col)
                        clicks.append(selectedSquare)
                    
                    if len(clicks) == 2:
                        res = getChessNotation(clicks[0], clicks[1])
                        move = chess.Move.from_uci(res)
                        myMove = GameEngine.MoveGenerator(clicks[0], clicks[1], ugly_board)
                        if move in board.legal_moves:
                            board.push(move)
                            moveMade = True
                            # print(board)
                        elif isPromotion(myMove) and not board.is_check():
                            board.push_san(str(move) + 'q')
                            moveMade = True
                        else:
                            clicks = [selectedSquare]
                        if (moveMade): # reset clicks
                            clicks = []
                            selectedSquare = ()
                            # print(board.legal_moves)
            elif not isWhitesTurn():
                minimax()

        updateBoard(screen, selectedSquare)
        pygame.display.flip()
