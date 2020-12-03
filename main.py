import chess
import pygame
import os
import random
from datetime import datetime, time
import time
import sys

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

pawn_eval_white = [
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

pawn_eval_black = pawn_eval_white[::-1]

knight_eval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishop_eval_white = [
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -3.0, -1.0, -1.0, -3.0, -1.0, -2.0]
]

bishop_eval_black = bishop_eval_white[::-1]

rook_eval_white = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0, 0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

rook_eval_black = rook_eval_white[::-1]

queen_eval = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

king_eval_white = [
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
]

king_eval_black = king_eval_white[::-1]

'''
# ADD TO ROOT
if 3 repetetive moves: do second best move
'''
def minimax_root(depth, board, is_white):
    # timer
    count = Stopwatch()
    count.start()

    leg_moves = board.legal_moves
    final_move = None
    best_value = 0
    if is_white:
        best_value = -9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            # print(value, move)
            if value > best_value:
                best_value = value
                final_move = move
                print(f"Value: {best_value}", end=" ")
                print(f"Move: {final_move}")
    else:
        best_value = 9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            # print(value, move)
            if value < best_value:
                best_value = value
                final_move = move
                print(f"Value: {best_value}", end=" ")
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
        total += getPieceValue(board.piece_at(i), i)
    return total

def getPieceValue(piece, i):
    '''
        0 -> [7][0]
        1 -> [7][1]
        8 -> [6][0]
        9 -> [6][1]
        16 -> [5][0]

        borde funka med
        [7 - i // 8][i % 8]

        24 -> [4][0] --> 7 - 24 // 8 == 3, 24 % 8 = 0
    '''

    if piece == None:
        return 0
    piece = str(piece)

    is_white = piece.isupper()

    multiplier = 1 if is_white else -1

    row = 7 - i // 8
    col = i % 8
    # assert row and col are the correct size?

    value = 0
    if piece == "P" or piece == "p":
        value = 10 + pawn_eval_white[row][col] if is_white else 10 + pawn_eval_black[row][col]
    elif piece == "N" or piece == "n":
        value = 30 + knight_eval[row][col]
    elif piece == "B" or piece == "b":
        value = 30 + bishop_eval_white[row][col] if is_white else 30 + bishop_eval_black[row][col]
    elif piece == "R" or piece == "r":
        value = 50 + rook_eval_white[row][col] if is_white else 50 + rook_eval_black[row][col]
    elif piece == "Q" or piece == "q":
        value = 90 + queen_eval[row][col]
    elif piece == 'K' or piece == 'k':
        value = 900 + king_eval_white[row][col] if is_white else 900 + king_eval_black[row][col]
    # print(f"p: {piece}\t val: {value*multiplier}\t at square: {chess.SQUARE_NAMES[i]}")
    return value * multiplier

def get_move(start, end):
    '''converts col row to chess notation i.e. 0,6 -> 0,5 becomes a2a3'''
    col_to_file = ['a','b','c','d','e','f','g','h']
    row_to_rank = ['8','7','6','5','4','3','2','1']

    start_sq = col_to_file[ start[0] ] + row_to_rank[ start[1] ]
    end_sq = col_to_file[ end[0] ] + row_to_rank[ end[1] ]

    return start_sq + end_sq

def init():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    return screen

def player_vs_ai(screen, board):

    game_over = False

    '''To get players move'''
    clicked_square = ()
    clicks = []

    # Player vs AI
    chosen_side = None
    while chosen_side not in {'w', 'b'}:
        chosen_side = input("Which color u play? w / b: ")

    while not game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    if len(board.move_stack) > 1:
                        board.pop()
                        board.pop()

            if board.is_checkmate():
                print("Checkmate!")
                game_over = True
                a = input("Press any key to exit...")
                break
            if board.is_stalemate():
                print("stalemate!")
                game_over = True
                a = input("Press any key to exit...")
                break

            if chosen_side == 'w':
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
                    draw_board(screen, board)
                    pygame.display.flip()
                else:
                    # Computer
                    print("--------------------------")
                    print("Computers turn")
                    print("--------------------------")
                    move = minimax_root(depth, board, False)
                    move = chess.Move.from_uci(str(move))
                    board.push(move)
                    draw_board(screen, board)
                    pygame.display.flip()
            elif chosen_side == 'b':
                g_Player = 'b'
                if board.turn:
                    # Computer
                    print("--------------------------")
                    print("Computers turn")
                    print("--------------------------")
                    # n == n + 1 depth
                    move = minimax_root(depth, board, True)
                    move = chess.Move.from_uci(str(move))
                    board.push(move)
                    draw_board(screen, board)
                    pygame.display.flip()
                else:
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
                    draw_board(screen, board)
                    pygame.display.flip()

g_Player = None

if __name__ == '__main__':

    screen = init()

    board = chess.Board()
    # board.set_fen("r1bqkb1r/ppp2ppp/2np1n2/4p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 5")

    # blit to screen once
    draw_board(screen, board)
    pygame.display.flip()
    
    # menu_option = None
    # while menu_option not in {"1", "2"}:
    #     menu_option = input("1. Player vs AI\n2. AI vs AI: ")
    menu_option = "1"

    depth = 0
    while depth < 2 or depth > 4:
        depth = int(input("Choose depth: 2-4 recommended: "))
    depth -= 1

    if menu_option == "1":
        player_vs_ai(screen, board)
    elif menu_option == "2":
        # AI vs AI
        while 1:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if board.turn:
                    # Computer
                    g_Player = 'b'
                    print("--------------------------")
                    print("White AI")
                    print("--------------------------")
                    if idx_moves < len(computer_opening):
                        board.push(computer_opening[idx_moves])
                        idx_moves += 1
                    else:
                        # n == n + 1 depth
                        move = minimax_root(depth, board)
                        move = chess.Move.from_uci(str(move))
                        board.push(move)
                        time.sleep(1)
                        draw_board(screen, board)
                        pygame.display.flip()
                else:
                    # Computer
                    g_Player = 'w'
                    print("--------------------------")
                    print("Black AI")
                    print("--------------------------")
                    if idx_moves < len(computer_opening):
                        board.push(computer_opening[idx_moves])
                        idx_moves += 1
                    else:
                        # n == n + 1 depth
                        move = minimax_root(depth, board)
                        move = chess.Move.from_uci(str(move))
                        board.push(move)
                        time.sleep(1)
                        draw_board(screen, board)
                        pygame.display.flip()
