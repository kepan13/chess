import chess
import pygame

import random
# from datetime import datetime, time
import sys

import eval
import pieces
import ai

'''
TODO:
    Null move pruning
    Check positions pruned by alpha beta vs all positions
    Add some things to eval, like bishops pair, passed pawns

    FOR ENDGAME:
        if piece_count < 7 ---> go to 7 depth or deeper... TRY THIS
'''

'''constants'''
WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

DEPTH = 4
PLAYER = 'w'

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
            pygame.draw.rect(screen, green, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
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

def player_vs_ai(screen, board):

    game_over = False

    '''To get players move'''
    clicked_square = ()
    clicks = []

    # Player vs AI
    chosen_side = PLAYER
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
                update_screen(screen, board)

            if board.is_checkmate():
                print("Checkmate!")
                # game_over = True
                a = input("'z': pop last move 'r': restart game:\n > ")
                if a == 'z':
                    board.pop()
                    board.pop()
                if a == 'r':
                    board.reset()
                # break
            if board.is_stalemate():
                print("stalemate!")
                # game_over = True
                a = input("'z': pop last move 'r': restart game\n > ")
                if a == 'z':
                    board.pop()
                    board.pop()
                if a == 'r':
                    board.reset()
                # break

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
                    print("--------------------------")
                    print("Computers turn")
                    print("--------------------------")
                    move = ai.minimax_root(depth, board, False)
                    move = chess.Move.from_uci(str(move))
                    board.push(move)
                    update_screen(screen, board)
            elif chosen_side == 'b':
                if not board.turn:
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
                    print("--------------------------")
                    print("Computers turn")
                    print("--------------------------")
                    if (len(opening)):
                        board.push(opening[0])
                        opening.pop()
                    else:
                        move = ai.minimax_root(depth, board, True)
                        move = chess.Move.from_uci(str(move))
                        board.push(move)
                    update_screen(screen, board)

if __name__ == '__main__':

    screen = init()

    board = chess.Board()
    # board.set_fen("r1bqkb1r/ppp2ppp/2np1n2/4p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 5")
    # board.set_fen("rr4k1/1pp2p1p/p5b1/3p4/1R1Pn1p1/P3P3/5PPP/4R1K1 w - - 0 28")
    # board.set_fen("1k6/ppp3pp/8/8/8/8/PPP3PP/1K6 w - - 0 28")

    # blit to screen once
    update_screen(screen, board)
    
    # menu_option = None
    # while menu_option not in {"1", "2"}:
    #     menu_option = input("1. Player vs AI\n2. AI vs AI: ")
    menu_option = "1"

    depth = DEPTH
    # while depth < 2 or depth > 4:
    #     depth = int(input("Choose depth: 2-4 recommended: "))
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
