import pygame
import GameEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION

IMAGES = {}


def load_images():
    pieces = ['br', 'bb', 'bn', 'bk', 'bq',
              'bp', 'wr', 'wb', 'wn', 'wk', 'wq', 'wp']

    for piece in pieces:
        IMAGES[piece] = pygame.image.load('pieces/' + piece + '.png')


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '.':
                screen.blit(IMAGES[piece], pygame.Rect(
                    c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def update_board(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)


# def make_move(game_engine, player_move):
#     origin = player_move[0]  # Comes as a tuple
#     destination = player_move[1]
#     piece_to_move = game_engine.board[origin[0]][origin[1]]
#     if piece_to_move == '.':
#         return

#     game_engine.board[origin[0]][origin[1]] = '.'
#     game_engine.board[destination[0]][destination[1]] = piece_to_move

#     game_engine.whiteTurn = not game_engine.whiteTurn  # Swaps turn


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color('white'))

    ge = GameEngine.GameEngine()
    load_images()
    game_over = False
    selected_square = ()
    player_clicks = []
    while not game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game_over = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                col = coord[0] // SQUARE_SIZE
                row = coord[1] // SQUARE_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    move = GameEngine.Move(
                        player_clicks[0], player_clicks[1], ge.board)
                    ge.make_move(move)
                    selected_square = ()
                    player_clicks = []
            update_board(screen, ge)
            pygame.display.flip()


if __name__ == '__main__':
    main()
