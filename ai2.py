import chess
import Stopwatch

INFINITY = 9999

kings_table = [
20, 30, 10,  0,  0, 10, 30, 20,
20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

endgame_kings_table = [
-30,-40,-30,-20,-20,-20,-40,-30,
-30,-30,-30,-30,-30,-30,-30,-30,
-10,-10, 20, 20, 20, 20,-10,-10,
 10, 10, 25, 25, 25, 25, 10, 10,
 20, 20, 20, 20, 20, 20, 20, 20,
 20, 20, 20, 20, 20, 20, 20, 20,
 20, 20, 20, 20, 20, 20, 20, 20,
 20, 20, 20, 20, 20, 20, 20, 20
]

pawns_table = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knights_table = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishops_table = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rooks_table = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queens_table = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

global moves_made

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

    pure_material = 100*(wp-bp) + 320*(wn-bn) + 350*(wb-bb) + 500*(wr-br) + 900*(wq-bq) + INFINITY*(wk-bk)

    pawn_pos = sum(pawns_table[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawn_pos += sum(-pawns_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))

    knight_pos = sum(knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knight_pos += sum(-knights_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))

    bishop_pos = sum(bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishop_pos += sum(-bishops_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))

    rook_pos = sum(rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rook_pos += sum(-rooks_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))

    queen_pos = sum(queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queen_pos += sum(-queens_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))

    kings_pos = 0
    if moves_made < 25:
        kings_pos = sum(kings_table[i] for i in board.pieces(chess.KING, chess.WHITE))
        kings_pos += sum(-kings_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))
    else:
        kings_pos = sum(endgame_kings_table[i] for i in board.pieces(chess.KING, chess.WHITE))
        kings_pos += sum(-endgame_kings_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))

    score = pure_material + pawn_pos + knight_pos + bishop_pos + rook_pos + queen_pos + kings_pos

    if board.turn:
        return score
    else:
        return -score

def quiescence_search(board : chess.Board, alpha : int, beta : int, max_depth : int) -> int:
    standard_eval = evaluation(board)
    if max_depth == 0:
        return standard_eval
    if standard_eval >= beta:
        return beta
    if alpha < standard_eval:
        alpha = standard_eval
    
    for move in board.legal_moves:
        piece = str(board.piece_at(move.from_square))
        if board.is_capture(move):
            if piece == 'q' or piece == 'Q':
                continue
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha, max_depth-1)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def negamax(board : chess.Board, alpha : int, beta : int, depth : int) -> int:
    best_score = -INFINITY
    if depth == 0:
        return quiescence_search(board, alpha, beta, 5)
        # return evaluation(board)
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth-1)
        board.pop()
        if score >= beta:
            return score
        if score > best_score:
            best_score = score
        if score > alpha:
            alpha = score
    return best_score

def find_move(board : chess.Board, depth : int) -> chess.Move:
    global moves_made
    moves_made = board.fullmove_number

    count = Stopwatch.Stopwatch()
    count.start()
    best_move = chess.Move.null()
    second_best_move = chess.Move.null()
    best_value = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth-1)
        if score > best_value:
            best_value = score
            second_best_move = best_move
            best_move = move
        if score > alpha:
            alpha = score
        board.pop()
    print("===================================")
    if board.is_repetition(2):
        print(f'second best move {second_best_move}', end="\n")
        if second_best_move is not chess.Move.null():
            return second_best_move
    print(f'Computer move {best_move} in {count.finish()}s')
    return best_move

