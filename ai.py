import chess
from datetime import datetime, time
import time
import sys

import eval

MAXINT = 10000

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

def minimax_root(depth, board):
    global nodes

    timer = Stopwatch()
    timer.start()

    cache = {}
    pv = {}

    for i in range(1, depth+1):
        inner_watch = Stopwatch()
        inner_watch.start()

        # if ai is white
        if board.turn:
            move, value = max_optim(i, board, -MAXINT, MAXINT, cache, pv)
        # if ai is black
        else:
            move, value = min_optim(i, board, -MAXINT, MAXINT, cache, pv)
        
        time_elapsed = inner_watch.finish()
        print(f"depth {i} took: {time_elapsed} sec")
        
    time = timer.finish()
    print(move)
    print("nodes: ", nodes)
    print(f"time: {time}s")
    nodes = 0
    return move


def max_optim(depth, board, alpha, beta, cache, pv):
    global nodes
    nodes += 1

    if depth == 0:
        return None, evaluation(board)

    best_value = -MAXINT
    best_move = None
    
    moves = list(board.legal_moves)
    # sorted_moves = sort_moves(board, moves)

    state = board.fen() + 'max'
    new_pv = []
    if state in cache:
        c_depth, val, move = cache[state]
        if move is not None and c_depth >= depth:
            return move, val
    if state in pv:
        _, pv_moves, _ = pv[state]
        moves = pv_moves + moves
    
    for i, i_move in enumerate(moves):
        move = chess.Move.from_uci(str(i_move))
        board.push(move)
        if board.is_fivefold_repetition() or board.is_repetition():
            board.pop()
            continue
        if board.is_stalemate():
            value = 0
        else:
            _, value = min_optim(depth - 1, board, alpha, beta, cache, pv)
        if value > best_value:
            best_value = value
            best_move = move
            new_pv.insert(0, i_move)
        board.pop()
        if value >= beta:
            break
        alpha = max(alpha, value)

    if state in cache:
        c_depth, val, move = cache[state]
        if c_depth < depth:
            cache[state] = (depth, best_value, best_move)
    else:
        cache[state] = (depth, best_value, best_move)
    
    if state in pv:
        c_depth, _, _, = pv[state]
        if c_depth < depth:
            pv[state] = (depth, new_pv, alpha)
    else:
        pv[state] = (depth, new_pv, alpha)

    return best_move, best_value

def min_optim(depth, board, alpha, beta, cache, pv):
    global nodes
    nodes += 1

    if depth == 0:
        return None, evaluation(board)

    best_value = MAXINT
    best_move = None


    moves = list(board.legal_moves)
    # sorted_moves = sort_moves(board, moves)

    state = board.fen() + 'min'
    new_pv = []
    if state in cache:
        c_depth, val, move = cache[state]
        if move is not None and c_depth >= depth:
            return move, val
    if state in pv:
        _, pv_moves, _ = pv[state]
        moves = pv_moves + moves

    for i, i_move in enumerate(moves):
        move = chess.Move.from_uci(str(i_move))
        board.push(move)
        if board.is_fivefold_repetition() or board.is_repetition():
            board.pop()
            continue
        if board.is_stalemate():
            value = 0
        else:
            _, value = max_optim(depth - 1, board, alpha, beta, cache, pv)
        if value < best_value:
            best_value = value
            best_move = move
            new_pv.insert(0, i_move)
        board.pop()
        if value <= alpha:
            break
        beta = min(beta, value)

    if state in cache:
        c_depth, val, move = cache[state]
        if c_depth < depth:
            cache[state] = (depth, best_value, best_move)
    else:
        cache[state] = (depth, best_value, best_move)
    
    if state in pv:
        c_depth, _, _ = pv[state]
        if c_depth < depth:
            pv[state] = (depth, new_pv, alpha)
    else:
        pv[state] = (depth, new_pv, alpha)

    return best_move, best_value

def sort_moves(board, moves):
    unsorted_moves = {}
    for move in moves:
        move = chess.Move.from_uci(str(move))
        board.push(move)
        value = evaluation(board)
        board.pop()
        unsorted_moves[move] = value
    # this sorts 2, 3, 4, 1 ---> 4, 3, 2, 1 Good or bad depending on max / min???
    # for max
    # sorted_moves = dict(reversed(sorted(unsorted_moves.items(), key=lambda item: item[1])))

    sorted_moves = None
    # for min
    if board.turn:
        sorted_moves = dict(reversed(sorted(unsorted_moves.items(), key=lambda item: item[1])))
    else:
        sorted_moves = dict(sorted(unsorted_moves.items(), key=lambda item: item[1]))
    ret = []
    # make a list
    for i in sorted_moves:
        ret.append(i)
    return ret



def evaluation(board):
    total = 0
    for i in range(64):
        total += getPieceValue(board.piece_at(i), i)
    return total

def getPieceValue(piece, i):
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
        value = 10 + eval.pawn_white[row][col] if is_white else 10 + eval.pawn_black[row][col]
    elif piece == "N" or piece == "n":
        value = 30 + eval.knight[row][col]
    elif piece == "B" or piece == "b":
        value = 35 + eval.bishop_white[row][col] if is_white else 35 + eval.bishop_black[row][col]
    elif piece == "R" or piece == "r":
        value = 50 + eval.rook_white[row][col] if is_white else 50 + eval.rook_black[row][col]
    elif piece == "Q" or piece == "q":
        value = 90 + eval.queen[row][col]
    elif piece == 'K' or piece == 'k':
        value = 900 + eval.king_white[row][col] if is_white else 900 + eval.king_black[row][col]
    # print(f"p: {piece}\t val: {value*multiplier}\t at square: {chess.SQUARE_NAMES[i]}")
    return value * multiplier