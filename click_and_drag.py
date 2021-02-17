import chess
import pygame
import pieces
import sys
import ai2
# first draw all squares and ranks / files
# different if computer moves and if player moves
white       = (255,255,255)
black       = (0, 0, 0)
gray        = (125, 125, 125)
cadet_blue  = (95, 158, 160)
burly_wood  = (222, 184, 135)
side_color = pygame.Color('Black')
# sq_size = 80
sq_size     = 100
from_color  = (153,153,0)
to_color    = (102,102,0)

LEFTCLICK = 1

pygame.init()
game_font = pygame.font.Font("04B_19.TTF",40)

dict_pieces = {'P': pieces.w_pawn, 'R': pieces.w_rook, 'N': pieces.w_knight, 'B': pieces.w_bishop, 'Q': pieces.w_queen, 'K': pieces.w_king, 'p': pieces.b_pawn, 'r': pieces.b_rook, 'n': pieces.b_knight, 'b': pieces.b_bishop, 'q': pieces.b_queen, 'k': pieces.b_king}

'''converts col row to chess notation i.e. 0,6 -> 0,5 becomes a2a3'''
def get_move(start, end):
    col_to_file = ['a','b','c','d','e','f','g','h']
    row_to_rank = ['8','7','6','5','4','3','2','1']

    start_sq = col_to_file[ start[0] ] + row_to_rank[ start[1] ]
    end_sq = col_to_file[ end[0] ] + row_to_rank[ end[1] ]

    return start_sq + end_sq


def draw_board(screen : pygame.Surface, board : chess.Board, move = chess.Move.null(), player_move=((-10,-10), (-10,-10))):
    colors = [pygame.Color('BurlyWood'), pygame.Color('Peru')]

    for row in range(8):
        # draw rank
        pygame.draw.rect(screen, side_color, (0, (row * sq_size), sq_size, sq_size))
        rank_text_surf = game_font.render(str(8 - row), True, white)
        rank_text_rect = rank_text_surf.get_rect(topleft=(30, (row*sq_size) + 30))
        screen.blit(rank_text_surf, rank_text_rect)
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (sq_size + col*sq_size, row*sq_size, sq_size, sq_size))
    
    # Print files & burly_wood square in the down-left corner
    files = ['a','b','c','d','e','f','g','h']
    pygame.draw.rect(screen, black, (0, 900-sq_size, sq_size, sq_size))
    for i in range(8):
        pygame.draw.rect(screen, side_color, (sq_size + i * sq_size, 900-sq_size, sq_size, sq_size))
        rank_text_surf = game_font.render(files[i], True, white)
        rank_text_rect = rank_text_surf.get_rect(bottomright=((sq_size + 70) + i*sq_size, 880))
        screen.blit(rank_text_surf, rank_text_rect)
    
    # draw highlighted squares
    if move == chess.Move.null():
        # player move
        from_sq = player_move[0]
        to_sq   = player_move[1]
        # Draw the origin with dark yellow and target sq with lighter yellow
        pygame.draw.rect(screen, from_color, (sq_size + from_sq[0]*sq_size, from_sq[1]*sq_size, sq_size, sq_size))
        pygame.draw.rect(screen, to_color, (sq_size + to_sq[0]*sq_size, to_sq[1]*sq_size, sq_size, sq_size))
    else:
        # computer move
        from_sq = move.from_square
        sq = from_sq
        row = 7 - sq // 8
        col = sq % 8
        from_sq = (col, row)

        to_sq = move.to_square
        sq = to_sq
        row = 7 - sq // 8
        col = sq % 8
        to_sq = (col, row)

        pygame.draw.rect(screen, from_color, (sq_size + from_sq[0]*sq_size, from_sq[1]*sq_size, sq_size, sq_size))
        pygame.draw.rect(screen, to_color, (sq_size + to_sq[0]*sq_size, to_sq[1]*sq_size, sq_size, sq_size))

    for i in chess.SQUARES:
        row = 7 - i // 8
        col = i % 8
        
        piece = str(board.piece_at(i))
        if board.piece_at(i) is not None:
            screen.blit(dict_pieces[piece], pygame.Rect(sq_size + col*sq_size, row*sq_size, sq_size, sq_size))

def main():
    button_clicked = False
    move_made = False
    origin_sq = (-1,-1)
    target_sq = (-1,-1)

    screen = pygame.display.set_mode((900, 900))
    board = chess.Board()

    draw_board(screen, board)

    board_state = []

    piece = ''
    while 1:
        if  not board.turn:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z:
                        if len(board_state) >= 2:
                            board_state.pop()
                            fen = board_state.pop()
                            board.set_fen(fen)
                        draw_board(screen, board)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == LEFTCLICK:
                        col, row = pygame.mouse.get_pos()
                        origin_sq = (abs(sq_size-col) // sq_size , row //sq_size )
                        # remove piece at square
                        square = abs(63 - (8 * origin_sq[1] - origin_sq[0] ) - 7)
                        piece = board.piece_at(square)
                        str_piece = str(piece)
                        board.remove_piece_at(square)
                        button_clicked = True
                    
                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == LEFTCLICK:
                        x, y = pygame.mouse.get_pos()
                        target_sq = (abs( sq_size-x) // sq_size, y // sq_size)
                        button_clicked = False
                        move_made = True

                if button_clicked and (str_piece != 'None'):
                    x, y = pygame.mouse.get_pos()
                    draw_board(screen, board)
                    screen.blit(dict_pieces[str_piece], pygame.Rect(x - 40, y - 40, sq_size, sq_size))
                        
            if not button_clicked and move_made:
                square = abs(63 - (8 * origin_sq[1] - origin_sq[0] ) - 7)
                board.set_piece_at(square, piece)
                player_move = get_move(origin_sq, target_sq)
                move = chess.Move.null()
                if origin_sq != target_sq:
                    move = chess.Move.from_uci(player_move)
                
                if move in board.legal_moves:
                    print(f"Player move {str(move)}")
                    # Custom move stack
                    board_state.append(board.fen())
                    board.push(move)
                    draw_board(screen, board, chess.Move.null(), (origin_sq, target_sq))
                elif target_sq[1] == 0 and str_piece == 'P':
                    move = chess.Move.from_uci(str(move)+'q')
                    board_state.append(board.fen())
                    board.push(move)
                    draw_board(screen, board, chess.Move.null(), (origin_sq, target_sq))
                else:
                    print("illegal move", move)
                    draw_board(screen, board)
                move_made = False
        else:
            computer_move = ai2.find_move(board, 3)
            board_state.append(board.fen())
            board.push(computer_move)
            draw_board(screen, board, computer_move)

        pygame.display.update()

main()
