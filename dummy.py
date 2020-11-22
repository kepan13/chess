import chess
import pygame
import os

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'pieces')

'''constants'''
WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

'''following code just loads and transforms the images to correct format'''
b_rook = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bR' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
b_knight = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bN' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
b_bishop = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bB' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
b_queen = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bQ' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
b_king = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bK' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
b_pawn = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'bp' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_rook = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wR' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_knight = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wN' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_bishop = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wB' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_queen = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wQ' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_king = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wK' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))
w_pawn = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'wp' + '.png')), (SQUARE_SIZE, SQUARE_SIZE))

dict_pieces = {'P': w_pawn, 'R': w_rook, 'N': w_knight, 'B': w_bishop, 'Q': w_queen, 'K': w_king, 'p': b_pawn, 'r': b_rook, 'n': b_knight, 'b': b_bishop, 'q': b_queen, 'k': b_king}

'''Main board'''
board = chess.Board()

'''Draws both squares and pieces'''
def draw_board(screen):
    a = board.fen()
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    row = 0
    col = 0
    print(a)
    for i in a:
        if i.isnumeric():
            '''Blank squares'''
            for j in range(int(i)):
                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                # print(f"From isnumeric() row: {row} col: {col}")
                col += 1

        elif i.isalpha():
            '''
            Letter in the FEN means piece on the board
            first draw square, then draw piece
            '''
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            screen.blit(dict_pieces[i], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # print(f"From isalpha() row: {row} col: {col}")
            col += 1

        elif i == ' ': # stop parsing, end of FEN
            return 0
        else: # means we reached a '\' and need to go down a row
            row += 1
            col = 0


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    draw_board(screen)
    pygame.display.flip()

    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()


