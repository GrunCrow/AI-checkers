import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK, GREY, BLUE, RED
from checkers.game import Game
from minimax.algorithm import minimax, alpha_beta_pruning, first_move
import time
import os

FPS = 60

ALPHA = float('-inf')
BETA = float('inf')

use_heuristic_white = True
use_heuristic_black = True

white_evaluate_function = 2
black_evaluate_function = 2
# 1 = evaluate_function_1 : depending on number of pawns and kings left
# 2 = evaluate_function_2: function_1 + depending on the side of the board

white_depth = 5
black_depth = 3

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

    white_total_time = 0
    black_total_time = 0

    white_counter = black_counter = 1

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            white_start_time = time.time()

            # Minimax
            # value, new_board = minimax(game.get_board(), white_depth, True, game, white_evaluate_function, WHITE, use_heuristic_white)

            # Alpha-Beta Pruning
            value, new_board = alpha_beta_pruning(game.get_board(), white_depth, ALPHA, BETA, True, game, white_evaluate_function, WHITE, use_heuristic_white)

            white_end_time = time.time()
            white_time = white_end_time - white_start_time
            white_total_time += white_time
            game.ai_move(new_board)
            print(f'White {white_counter} move time: {white_time}')
            white_counter += 1
        '''elif game.turn == BLACK:
            if black_counter == 1:
                new_board = first_move(game.get_board(), game)
                game.ai_move(new_board)
                black_time = 0
            else:

                black_start_time = time.time()

                # Minimax
                # value, new_board = minimax(game.get_board(), black_depth, True, game, black_evaluate_function, BLACK, use_heuristic_black)

                # Alpha-Beta Pruning
                value, new_board = alpha_beta_pruning(game.get_board(), black_depth, ALPHA, BETA, True, game, black_evaluate_function, BLACK, use_heuristic_black)

                black_end_time = time.time()
                black_time = black_end_time - black_start_time
                black_total_time += black_time
                game.ai_move(new_board)

            print(f'Black {black_counter} move time: {black_time}')
            black_counter += 1'''

        if game.winner() is not None:
            if game.winner() is not GREY:
                print('Winner is: ')
                if game.winner() == BLACK or game.winner() == BLUE:
                    print('BLACK (AI)')
                elif game.winner() == WHITE or game.winner() == RED:
                    print('WHITE (AI)')
                else:
                    print(game.winner())
            else:
                print('Draw')

            print(f'White total time: {white_total_time}')
            print(f'Black total time: {black_total_time}')
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    os.system("pause")

    pygame.quit()


main()
