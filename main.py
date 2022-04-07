import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from checkers.game import Game
from minimax.algorithm import minimax
import time

FPS = 60

depth = 3

evaluate_function = 2
# 1 = evaluate_function_1 : without kings
# 2 = evaluate_function_2: with kings + heuristics

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    white_counter = black_counter = 1

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            white_start_time = time.time()
            value, new_board = minimax(game.get_board(), depth, True, game, 1, WHITE)
            white_end_time = time.time()
            white_time = white_end_time - white_start_time
            game.ai_move(new_board)
            print(f'White {white_counter} move time: {white_time}')
            white_counter += 1
        elif game.turn == BLACK:
            black_start_time = time.time()
            value, new_board = minimax(game.get_board(), depth, True, game, 2, BLACK)
            black_end_time = time.time()
            black_time = black_end_time - black_start_time
            game.ai_move(new_board)
            print(f'Black {black_counter} move time: {black_time}')
            black_counter += 1

        if game.winner() is not None:
            print('Winner is: ')
            winner = game.winner()
            if game.winner() == BLACK:
                print('BLACK (AI)')
            elif game.winner() == WHITE:
                print('WHITE (AI)')
            else:
                print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()
