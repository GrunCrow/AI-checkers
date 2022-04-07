import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from checkers.game import Game
from minimax.algorithm import minimax

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

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), depth, True, game, 2, WHITE)
            game.ai_move(new_board)
        elif game.turn == BLACK:
            value, new_board = minimax(game.get_board(), depth, True, game, 1, BLACK)
            game.ai_move(new_board)

        if game.winner() is not None:
            print('Winner is: ')
            if game.winner == BLACK:
                print('BLACK (HUMAN)')
            elif game.winner == WHITE:
                print('WHITE (AI)')
            else:
                print('Error')
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
