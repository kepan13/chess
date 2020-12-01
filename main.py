import chess
import pygame
import os
import random
from datetime import datetime, time

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

'''Fill a dict with square names. key = chess.SQUARE_NAMES i.e. a1 a2... value = chess.SQUARES chess.A1 chess.A2...'''
dict_squares = {}


class Stopwatch(object):
    def __init__(self):
        self.start_time = None
    
    def start(self):
        self.start_time = datetime.now()
    @property
    def value(self):
        return (datetime.now() - self.start_time).total_seconds()
    def peek(self):
        return self.value
    def finish(self):
        return self.value

'''Draws both squares and pieces'''
def draw_board(screen, board):
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


def fill_squares_dict():
    for i in range(64):
        dict_squares[chess.SQUARE_NAMES[i]] = chess.SQUARES[i]

'''
rank 1
rank 2
rank 3
...
...
rank 8
'''
# knight_eval = 
# [
# -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
# -4.0, -2.0, -0.0, 0.5, 0.5, 0.5, 0.0, -2.0, -4.0,
# -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0,
# -3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0,
# -3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0,
# -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0,
# -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0,
# -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
# ] # white right now, reverse for black

def minimax_root(depth, board):
    # timer
    count = Stopwatch()
    count.start()

    leg_moves = board.legal_moves
    final_move = None
    best_value = -9999
    for i_move in leg_moves:
        move = chess.Move.from_uci(str(i_move))
        board.push(move)
        value = minimax(depth, board, -10000, 10000, False)
        board.pop()
        # print(value, move)
        if value > best_value:
            best_value = value
            final_move = move
            print(f"Value: {best_value}")
            print(f"Move: {final_move}")
    time_elapsed = count.finish()
    print(f"time spent: {time_elapsed}s")
    return final_move

def minimax(depth,board, alpha, beta, is_max):
    if depth == 0:
        return evaluation(board)
    leg_moves = board.legal_moves
    if is_max:
        value = -9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = max(value, minimax(depth - 1, board, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if beta <= alpha:
                return value
        return value
    else:
        value = 9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = min(value, minimax(depth - 1, board, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if(beta <= alpha):
                return value
        return value




def evaluation(board):
    total = 0
    for i in range(64):
        total += getPieceValue(board.piece_at(i))
    return total

def getPieceValue(piece):
    piece = str(piece)
    if(piece == None):
        return 0
    multiplier = 1
    if piece.isupper():
        multiplier = -1
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    elif piece == "N" or piece == "n":
        value = 30
    elif piece == "B" or piece == "b":
        value = 30
    elif piece == "R" or piece == "r":
        value = 50
    elif piece == "Q" or piece == "q":
        value = 90
    elif piece == 'K' or piece == 'k':
        value = 900
    return value * multiplier

def get_move(start, end):
    '''converts col row to chess notation i.e. 0,6 -> 0,5 becomes a2a3'''
    col_to_file = ['a','b','c','d','e','f','g','h']
    row_to_rank = ['8','7','6','5','4','3','2','1']

    start_sq = col_to_file[ start[0] ] + row_to_rank[ start[1] ]
    end_sq = col_to_file[ end[0] ] + row_to_rank[ end[1] ]

    return start_sq + end_sq

def get_piece(board, move):
    ''' returns piece taken kind of
        capital letter -> black piece
        else           -> white piece '''
    move = str(move)[2:]
    return board.piece_at(dict_squares[move])

def random_move(board):
    for x in board.legal_moves:
        return x

'''Opening for computer'''
idx_moves = 0
computer_opening = [chess.Move.from_uci("g8f6"), chess.Move.from_uci("g7g6"), chess.Move.from_uci("d7d6"), chess.Move.from_uci("f8g7"), chess.Move.from_uci("e8g8")]

if __name__ == '__main__':
    # maybe make a general init()
    fill_squares_dict()
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    
    board = chess.Board()
    # board.set_fen("r1bqkb1r/ppp2ppp/2np1n2/4p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 5")

    '''To get players move'''
    clicked_square = ()
    clicks = []

    draw_board(screen, board)
    pygame.display.flip()

    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    if len(board.move_stack) > 1:
                        board.pop()
                        board.pop()
            if board.turn:
                # Player
                if e.type == pygame.MOUSEBUTTONDOWN:
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
                        draw_board(screen, board)
                        pygame.display.flip()
                    else:
                        clicks = [clicked_square]
                # draw_board(screen, board)
                # pygame.display.flip()
            else:
                # Computer
                print("--------------------------")
                print("Computers turn")
                print("--------------------------")
                if idx_moves < 5:
                    board.push(computer_opening[idx_moves])
                    idx_moves += 1
                else:
                    # n == n + 1 depth
                    move = minimax_root(3, board)
                    move = chess.Move.from_uci(str(move))
                    board.push(move)
            draw_board(screen, board)
            pygame.display.flip()
