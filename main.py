import chess
import pygame

import random
import sys

import eval
import pieces
import ai
import ai2

'''constants'''
WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

DEPTH = 3

dict_pieces = {'P': pieces.w_pawn, 'R': pieces.w_rook, 'N': pieces.w_knight, 'B': pieces.w_bishop, 'Q': pieces.w_queen, 'K': pieces.w_king, 'p': pieces.b_pawn, 'r': pieces.b_rook, 'n': pieces.b_knight, 'b': pieces.b_bishop, 'q': pieces.b_queen, 'k': pieces.b_king}


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

def update_screen(screen, board, *start_sq):
    if start_sq:
        draw_board(screen, board, start_sq)
    else:
        draw_board(screen, board)
    pygame.display.flip()

def draw_board(screen, board, *start_sq):
    '''
    Draws board, highlights possible moves for clicked piece and highlights when checked.
    '''
    colors = [pygame.Color('navajowhite1'), pygame.Color('peru')]
    green =  pygame.Color('yellowgreen')
    blue = pygame.Color('blue')
    red = (255,0,0)
    red = pygame.Color('red4')
    b_king_square = None
    w_king_square = None
    highlighted_pieces = []
    legal_moves = [str(legal_move) for legal_move in board.legal_moves]
    highight_size = SQUARE_SIZE - 10
    
    selected_square = None
    if start_sq:
        selected_square = get_move(start_sq[0][0], (0,0))[:2]
    for move in legal_moves:
        if move[0:2] == selected_square:
            highlighted_pieces.append(chess.SQUARE_NAMES.index(move[2:4]))

    for square in chess.SQUARES:
        row = 7 - square // 8
        col = square % 8
        color = colors[(row + col) % 2]
        piece = str(board.piece_at(square))

        if piece == 'k':
            b_king_square = square
        if piece == 'K':
            w_king_square = square
        if square in highlighted_pieces:
            pygame.draw.rect(screen, green, (col*SQUARE_SIZE + 20, row*SQUARE_SIZE + 20, SQUARE_SIZE - 40, SQUARE_SIZE - 40))
        else:
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if board.piece_at(square) is not None:
            screen.blit(dict_pieces[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if board.is_check():
        if board.turn:
            # White king under attack!
            row = 7 - w_king_square // 8
            col = w_king_square % 8
            pygame.draw.rect(screen, red, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(dict_pieces['K'], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
            # Black king under attack!
            row = 7 - b_king_square // 8
            col = b_king_square % 8
            pygame.draw.rect(screen, red, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(dict_pieces['k'], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

opening = [chess.Move.from_uci("d2d4")]

def game_over_menu(board):
    print("GAME OVER!")
    # game_over = True
    a = input("'z': pop last move 'r': restart game 'q': quit\n > ")
    if a == 'z':
        board.pop()
        board.pop()
    if a == 'r':
        board.reset()
    if a == 'q':
        sys.exit(1)

def player_vs_ai(screen, board):

    game_over = False

    '''To get players move'''
    clicked_square = ()
    clicks = []

    depth = DEPTH

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
                update_screen(screen, board)

            if board.is_checkmate():
                game_over_menu(board)
            if board.is_stalemate():
                game_over_menu(board)
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
                        from_square = clicks[0]
                        update_screen(screen, board, from_square)

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
                    update_screen(screen, board)
            else:
                # Computer
                # move = ai.minimax_root(depth, board, False)
                # # move = chess.Move.from_uci(str(move))
                # board.push(move)
                move = ai2.find_move(board, DEPTH)
                board.push(move)
                update_screen(screen, board)


if __name__ == '__main__':

    screen = init()

    board = chess.Board()

    # blit to screen once
    update_screen(screen, board)

    # game loop
    player_vs_ai(screen, board)
    # while 1:
    #     m = ai2.find_move(board, DEPTH)
    #     board.push(m)
    #     update_screen(screen, board)
