import chess
from datetime import datetime, time
import time

import eval

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

nodes = 0

def minimax_root(depth : int, board : chess.Board, is_white : bool) -> None:
    global nodes

    # timer
    count = Stopwatch()
    count.start()

    nodes = 0
    third_best = None
    second_best = None
    leg_moves = board.legal_moves
    final_move = None
    best_value = 0
    
    # the root is of depth 1
    depth -= 1

    if is_white:
        best_value = -9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            if value > best_value:
                best_value = value
                third_best = second_best
                second_best = final_move
                final_move = move
    else:
        best_value = 9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            if value < best_value:
                best_value = value
                third_best = second_best
                second_best = final_move
                final_move = move
    time_elapsed = count.finish()
    print(f"nodes: {nodes}    value: {best_value}")
    print(f"best move: {final_move}")
    print(f"time spent: {time_elapsed}s")

    if final_move is not None:
        board.push(final_move)
    else:
        for move in leg_moves:
            return move
        
    if board.is_repetition() and second_best is not None:
        print("Made 2nd best move due to repetition")
        board.pop()
        return second_best
    board.pop()
    return final_move

def minimax(depth : int, board : chess.Board, alpha : int, beta : int, is_max : bool) -> int:
    global nodes

    if depth == 0:
        nodes += 1
        return quiescence_search(board, alpha, beta)

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
                break
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
                break
        return value

# def evaluation(board):
#     total = 0
#     for i in range(64):
#         total += getPieceValue(board.piece_at(i), i)
#     return total

# def getPieceValue(piece, i):
#     if piece == None:
#         return 0
#     piece = str(piece)

#     is_white = piece.isupper()

#     multiplier = 1 if is_white else -1

#     row = 7 - i // 8
#     col = i % 8
#     # assert row and col are the correct size?

#     value = 0
#     if piece == "P" or piece == "p":
#         value = 10 + eval.pawn_white[row][col] if is_white else 10 + eval.pawn_black[row][col]
#     elif piece == "N" or piece == "n":
#         value = 30 + eval.knight[row][col]
#     elif piece == "B" or piece == "b":
#         value = 30 + eval.bishop_white[row][col] if is_white else 30 + eval.bishop_black[row][col]
#     elif piece == "R" or piece == "r":
#         value = 50 + eval.rook_white[row][col] if is_white else 50 + eval.rook_black[row][col]
#     elif piece == "Q" or piece == "q":
#         value = 90 + eval.queen[row][col]
#     elif piece == 'K' or piece == 'k':
#         value = 900 + eval.king_white[row][col] if is_white else 900 + eval.king_black[row][col]
#     # print(f"p: {piece}\t val: {value*multiplier}\t at square: {chess.SQUARE_NAMES[i]}")
#     return value * multiplier

def evaluation(board : chess.Board) -> int:
    # material score
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wk = len(board.pieces(chess.KING, chess.WHITE))
    bk = len(board.pieces(chess.KING, chess.BLACK))

    pure_material = 100*(wp-bp) + 320*(wn-bn) + 350*(wb-bb) + 500*(wr-br) + 900*(wq-bq) + 9999*(wk-bk)

    pawn_pos = sum(eval.pawns_table[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawn_pos += sum(-eval.pawns_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))

    knight_pos = sum(eval.knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knight_pos += sum(-eval.knights_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))

    bishop_pos = sum(eval.bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishop_pos += sum(-eval.bishops_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))

    rook_pos = sum(eval.rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rook_pos += sum(-eval.rooks_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))

    queen_pos = sum(eval.queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queen_pos += sum(-eval.queens_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))

    kings_pos = sum(eval.kings_table[i] for i in board.pieces(chess.KING, chess.WHITE))
    kings_pos += sum(-eval.kings_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))

    score = pure_material + pawn_pos + knight_pos + bishop_pos + rook_pos + queen_pos + kings_pos

    if board.turn:
        return score
    else:
        return -score

def quiescence_search(board : chess.Board, alpha : int, beta : int) -> int:
    standard_eval = evaluation(board)
    if standard_eval >= beta:
        return beta
    if alpha < standard_eval:
        alpha = standard_eval
    
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha