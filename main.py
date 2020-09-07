import chess
import pygame
import GameEngine

def getChessNotation(startSq, endSq):

    intToFile = {0:'a', 1:'b', 2:'c', 3:'d', 4: 'e',
                5: 'f', 6:'g', 7:'h'}
    intToRank = {0: '8',1: '7', 2: '6', 3: '5', 4: '4',
                5: '3', 6: '2', 7: '1'}
    return intToFile[startSq[1]] + intToRank[startSq[0]] + intToFile[endSq[1]] + intToRank[endSq[0]]

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
IMAGES = {}
moveLog = []


ugly_board = [
                ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['..', '..', '..', '..','..', '..', '..', '..'],
                ['..', '..', '..', '..','..', '..', '..', '..'],
                ['..', '..', '..', '..','..', '..', '..', '..'],
                ['..', '..', '..', '..','..', '..', '..', '..'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
            ]

def loadImages():
    pieces = ['bR', 'bB', 'bN', 'bK', 'bQ',
              'bp', 'wR', 'wB', 'wN', 'wK', 'wQ', 'wp']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('pieces/' + piece + '.png')
        IMAGES[piece] = pygame.transform.scale(
            IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))


def drawBoard(screen):
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = ugly_board[r][c]
            if piece != '..':
                screen.blit(IMAGES[piece], pygame.Rect( c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def updateBoard(screen):
    drawBoard(screen)
    drawPieces(screen)

def make_move(startSq, endSq):
    move = GameEngine.MoveGenerator(startSq, endSq, ugly_board)
    # startRow = startSq[0]
    # startCol = startSq[1]
    # endRow = endSq[0]
    # endCol = endSq[1]
    ugly_board[move.startRow][move.startCol] = '..'
    ugly_board[move.endRow][move.endCol] = move.pieceMoved

    moveLog.append(move)

def undoMove():
    move = moveLog.pop()
    ugly_board[move.startRow][move.startCol] = move.pieceMoved
    ugly_board[move.endRow][move.endCol] = move.pieceCaptured
    


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

board = chess.Board()
print(board)
loadImages()
selectedSquare = ()
clicks = []
print(board.legal_moves)
while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
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
                
                if move in board.legal_moves:
                    make_move(clicks[0], clicks[1])
                    board.push(move)
                    clicks = []
                    selectedSquare = ()
                    print(board.legal_moves)
                else:
                    clicks = [selectedSquare]
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_z:
                # undo move
                if len(moveLog):
                    board.pop()
                    undoMove()
                    print(board)


    updateBoard(screen)
    pygame.display.flip()
