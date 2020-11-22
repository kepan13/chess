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
    for i in a:
        if i.isnumeric():
            '''Blank squares'''
            for j in range(int(i)):
                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                col += 1

        elif i.isalpha():
            '''
            Letter in the FEN means piece on the board
            first draw square, then draw piece
            '''
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            screen.blit(dict_pieces[i], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            col += 1

        elif i == ' ': # stop parsing, end of FEN
            return 0
        else: # means we reached a '\' and need to go down a row
            row += 1
            col = 0

def get_move(start, end):
    '''converts col row to chess notation i.e. 0,6 -> 0,5 becomes a2a3'''
    col_to_file = ['a','b','c','d','e','f','g','h']
    row_to_rank = ['8','7','6','5','4','3','2','1']

    start_sq = col_to_file[ start[0] ] + row_to_rank[ start[1] ]
    end_sq = col_to_file[ end[0] ] + row_to_rank[ end[1] ]

    return start_sq + end_sq

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])


    '''To get players move'''
    clicked_square = ()
    clicks = []

    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            
            elif e.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if clicked_square == (col, row):
                    clicked_square = ()
                    clicks = []
                else:
                    clicked_square = (col, row)
                    clicks.append(clicked_square)
            
            if len(clicks) == 2:
                move = get_move(clicks[0], clicks[1])
                move = chess.Move.from_uci(move)
                if move in board.legal_moves:
                    board.push(move)
                    clicks = []
                    clicked_square = []
                elif chess.Move.from_uci(str(move)+'q') in board.legal_moves:
                '''Check if it is promotion time'''
                    move = chess.Move.from_uci(str(move)+'q')
                    board.push(move)
                    clicks = []
                    clicked_square = []
                else:
                    clicks = [clicked_square]
        draw_board(screen)
        pygame.display.flip()