import pygame
import GameEngine

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
IMAGES = {}


def drawBoard(screen):
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # (r+c) % 2 == 0 --> white
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (row*SQUARE_SIZE,
                                             col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(
                    c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def loadImages():
    pieces = ['br', 'bb', 'bn', 'bk', 'bq',
              'bp', 'wr', 'wb', 'wn', 'wk', 'wq', 'wp']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('pieces/' + piece + '.png')
        IMAGES[piece] = pygame.transform.scale(
            IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))


def updateBoard(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)


def display(board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            print(board[r][c], end=" ")
        print()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Chess by Oscar')
    loadImages()
    playerClicks = []
    selectedSquare = ()
    legalMoves = []
    gs = GameEngine.GameEngine()
    while 1:

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                col = coord[0] // SQUARE_SIZE
                row = coord[1] // SQUARE_SIZE
                # If player clicks the same square twice
                if selectedSquare == (row, col):
                    selectedSquare = ()
                    playerClicks = []
                else:
                    selectedSquare = (row, col)
                    playerClicks.append(selectedSquare)

                # square to move from is selected, show all legal moves for this piece
                if len(playerClicks) == 1:
                    legalMoves = gs.getAllLegalMoves(playerClicks[0])

                if len(playerClicks) == 2:
                    move = gs.getChessNotation(
                        (playerClicks[0]), (playerClicks[1]))
                    if move in legalMoves:
                        # make move
                        gs.makeMove(playerClicks)

                    # Reset square and clicks
                    selectedSquare = ()
                    playerClicks = []
                    legalMoves = []

            updateBoard(screen, gs)
            pygame.display.flip()
