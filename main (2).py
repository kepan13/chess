import chess
import pygame
import os
import random
from datetime import datetime, time
from threading import Thread
import math
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'pieces')

'''constants'''
WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAXINT = 10000
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

nodes = 0
no_pruning_nodes = 0
no_caching_nodes = 0

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

pawn_eval_black = [k[::-1] for k in pawn_eval_white][::-1]

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
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishop_eval_black = [k[::-1] for k in bishop_eval_white][::-1]

rook_eval_white = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

rook_eval_black = [k[::-1] for k in rook_eval_white][::-1]

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

king_eval_black = [k[::-1] for k in king_eval_white][::-1]


'''Fill a dict with square names. key = chess.SQUARE_NAMES i.e. a1 a2... value = chess.SQUARES chess.A1 chess.A2...'''

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

def minimax_root(depth, board):
  stop_watch = Stopwatch()
  stop_watch.start()
  pv = {}
  cache = {}
  for i in range(1, depth+1):
    inner_watch = Stopwatch()
    inner_watch.start()
    
    move, value = max_optim(i, board, -MAXINT, MAXINT, cache, pv)

    time_elapsed = inner_watch.finish()
    print(f"depth {i} took: {time_elapsed}s")
  time_elapsed = stop_watch.finish()
  print(f"time spent: {time_elapsed}s")
 
  

  stop_watch = Stopwatch()
  stop_watch.start()
  # move_no_pruning, value = max_optim_no_pruning(depth, board)
  # no_cache_move, _ = max_optim_no_caching(depth, board, -MAXINT, MAXINT)
  time_elapsed = stop_watch.finish()
  print(f"time spent: {time_elapsed}s")
  print(move)
  return move


def max_optim(depth, board, alpha, beta, cache, pv):
  global nodes
  nodes += 1
  
  if depth == 0:
    return None, evaluation(board)
  best_value = -MAXINT
  best_move = None

  moves = list(board.legal_moves)
  state = board.fen() + 'max'
  new_pv = []

  if state in cache:
    cache_depth, value, move = cache[state]
    if move is not None and cache_depth >= depth:
      return move, value
  
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
      
      if (value > best_value):
        best_value = value
        best_move = move
        new_pv.insert(0, i_move)

      board.pop()
      if value >= beta:
        break
      alpha = max(alpha, value)
   
  if state in cache:
    cache_depth, value, move = cache[state]
    if cache_depth < depth:
      cache[state] = (depth, best_value, best_move)
  else:
    cache[state] = (depth, best_value, best_move)

  if state in pv:
    cache_depth, _, _ = pv[state]
    if cache_depth < depth:
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
  best_uci_move = None
  state = board.fen() + 'min'

  new_pv = []
  moves = list(board.legal_moves)

 
  if state in cache:
    cache_depth, value, move = cache[state]
    if move is not None and cache_depth >= depth:
      return move, value
  
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
      
      if (value < best_value):
        best_value = value
        best_move = move
        new_pv.insert(0, i_move)
      board.pop()
      if value <= alpha:
        break
      beta = min(beta, value)
  

  if state in cache:
    cache_depth, value, move = cache[state]
    if cache_depth < depth:
      cache[state] = (depth, best_value, best_move)
  else:
    cache[state] = (depth, best_value, best_move)

  if state in pv:
    cache_depth, _, _ = pv[state]
    if cache_depth < depth:
      pv[state] = (depth, new_pv, alpha)
  else:
    pv[state] = (depth, new_pv, alpha)

  return best_move, best_value

def max_optim_no_pruning(depth, board):
  global no_pruning_nodes
  no_pruning_nodes += 1
  
  if depth == 0:
    return None, evaluation(board)
  best_value = -MAXINT
  best_move = None

  moves = list(board.legal_moves)

  for i, i_move in enumerate(moves):
      move = chess.Move.from_uci(str(i_move))
      board.push(move)
      _, value = min_optim_no_pruning(depth - 1, board)
      if (value > best_value):
        best_value = value
        best_move = move
      
      board.pop()

  return best_move, best_value

def min_optim_no_pruning(depth, board):
  global no_pruning_nodes
  no_pruning_nodes += 1

  if depth == 0:
    return None, evaluation(board)
  best_value = MAXINT
  best_move = None

  moves = list(board.legal_moves)
  
  
  for i, i_move in enumerate(moves):
      move = chess.Move.from_uci(str(i_move))
      board.push(move)
      _, value = max_optim_no_pruning(depth - 1, board)
      if (value < best_value):
        best_value = value
        best_move = move
      
      board.pop()
  
  return best_move, best_value

def max_optim_no_caching(depth, board, alpha, beta):
  global no_caching_nodes
  no_caching_nodes += 1
  
  if depth == 0:
    return None, evaluation(board)
  best_value = -MAXINT
  best_move = None

  moves = list(board.legal_moves)

  for i, i_move in enumerate(moves):
      move = chess.Move.from_uci(str(i_move))
      board.push(move)
      _, value = min_optim_no_caching(depth - 1, board, alpha, beta)
      if (value > best_value):
        best_value = value
        best_move = move
     
      board.pop()
      if value >= beta:
        break
      alpha = max(alpha, value)
     
  return best_move, best_value

def min_optim_no_caching(depth, board, alpha, beta):
  global no_caching_nodes
  no_caching_nodes += 1

  if depth == 0:
    return None, evaluation(board)
  best_value = MAXINT
  best_move = None

  moves = list(board.legal_moves)
  
  
  for i, i_move in enumerate(moves):
      move = chess.Move.from_uci(str(i_move))
      board.push(move)
      _, value = min_optim_no_caching(depth - 1, board, alpha, beta)
      if (value < best_value):
        best_value = value
        best_move = move
      
      board.pop()
      if value <= alpha:
        break
      beta = min(beta, value)
  return best_move, best_value


def evaluation(board):
    total = 0
    
    if board.is_checkmate():
      return MAXINT if board.turn else -MAXINT
    
    for i in range(64):
      total += get_piece_value(board.piece_at(i), i)
    return total

def get_piece_value(piece, i):
  piece = str(piece)
  if(piece == None):
    return 0
  multiplier = 1
  whites_turn = False
  if piece.isupper():
    whites_turn = True
    multiplier = -1
  x = 7 - i // 8
  y = i % 8
  value = 0
  if piece == "P" or piece == "p":
    value = 10 + (pawn_eval_white[x][y] if whites_turn else pawn_eval_black[x][y])
  elif piece == "N" or piece == "n":
    value = 30 + knight_eval[x][y]
  elif piece == "B" or piece == "b":
    value = 30 + (bishop_eval_white[x][y] if whites_turn else bishop_eval_black[x][y])
  elif piece == "R" or piece == "r":
    value = 50 + (rook_eval_white[x][y] if whites_turn else rook_eval_black[x][y])
  elif piece == "Q" or piece == "q":
    value = 90 + queen_eval[x][y]
  elif piece == 'K' or piece == 'k':
    value = 900 + (king_eval_white[x][y] if whites_turn else king_eval_black[x][y])
  return value * multiplier

def get_move(start, end):
  '''converts col row to chess notation i.e. 0,6 -> 0,5 becomes a2a3'''
  col_to_file = ['a','b','c','d','e','f','g','h']
  row_to_rank = ['8','7','6','5','4','3','2','1']

  start_sq = col_to_file[ start[0] ] + row_to_rank[ start[1] ]
  end_sq = col_to_file[ end[0] ] + row_to_rank[ end[1] ]

  return start_sq + end_sq

def random_move(board):
  for x in board.legal_moves:
    return x

'''Opening for computer'''
idx_moves = 0
# computer_opening = [chess.Move.from_uci("g8f6"), chess.Move.from_uci("g7g6"), chess.Move.from_uci("d7d6"), chess.Move.from_uci("f8g7"), chess.Move.from_uci("e8g8")]

if __name__ == '__main__':
  # maybe make a general init()
  pygame.init()
  screen = pygame.display.set_mode([WIDTH, HEIGHT])
  
  board = chess.Board()
  # board.set_fen("r1bqkb1r/ppp2ppp/2np1n2/4p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 5")

  '''To get players move'''
  clicked_square = ()
  clicks = []

  draw_board(screen, board)
  pygame.display.flip()
  cache = {}
  while 1:
    for e in pygame.event.get():
      if board.turn:
        if e.type == pygame.KEYDOWN:
          if e.key == 32:
            if len(board.move_stack) > 1:
                board.pop()
                board.pop()
                draw_board(screen, board)
                pygame.display.flip()
                      # Player
          if(e.key == 113):
            exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
          (x, y) = pygame.mouse.get_pos()
          col = x // SQUARE_SIZE
          row = y // SQUARE_SIZE
          if clicked_square != (col, row):
            clicked_square = (col, row)
            clicks.append(clicked_square)
          if len(clicks) == 2:
            move = get_move(clicks[0], clicks[1])
            move = chess.Move.from_uci(move)
            clicks = []
            clicked_square = ()
            if move in board.legal_moves:
              board.push(move)
              draw_board(screen, board)
              pygame.display.flip()
              continue

    if not board.turn:
      # Computer
      print("--------------------------")
      print("Computers turn")
      print("--------------------------")
      nodes = 0
      no_pruning_nodes = 0
      no_cache_nodes = 0
      move = minimax_root(4, board)
      print(nodes)
      print(no_pruning_nodes)
      print(no_caching_nodes)
      move = chess.Move.from_uci(str(move))
      board.push(move)
      draw_board(screen, board)
      pygame.display.flip()