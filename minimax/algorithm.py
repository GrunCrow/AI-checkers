from copy import deepcopy   # to avoid changing a copy of the board and modify the original object and all
import pygame

from checkers.constants import WHITE, GREEN


def minimax(position, depth, max_player, game, evaluate_function=1, ai_color=WHITE):
    #   position = board current position (origin)
    #   depth = how depth is the tree going to be
    #   max_player = if we are min or max the value (boolean)
    #   game = game object

    #   evaluation starts at the bottom of the tree
    if depth == 0 or position.winner() is not None:
        if evaluate_function == 1:
            return position.evaluate_function_1(ai_color), position
        elif evaluate_function == 2:
            return position.evaluate_function_2(ai_color), position

    if max_player:  # max the score
        max_eval = float('-inf')     # init at -inf
        best_move = None
        for move in get_all_moves(position, ai_color, game):   # for every possible move
            evaluation = minimax(move, depth-1, False, game, evaluate_function, ai_color)[0]    # next = min
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move

    else:   # min the score
        min_eval = float('inf')  # init at inf for minimizing
        best_move = None
        for move in get_all_moves(position, ai_color, game):
            evaluation = minimax(move, depth - 1, True, game, evaluate_function, ai_color)[0]  # next = max
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move


def alpha_beta_pruning(position, depth, max_player, game, evaluate_function=2):
    #   position = board current position (origin)
    #   depth = how depth is the tree going to be
    #   max_player = if we are min or max the value (boolean)
    #   game = game object

    #   evaluation starts at the bottom of the tree
    if depth == 0 or position.winner() is not None:
        position_winner = position.winner()
        evaluate = position.evaluate_function_1()
        if evaluate_function == 1:
            return position.evaluate_function_1(), position
        elif evaluate_function == 2:
            return position.evaluate_function_2(), position

    if max_player:  # max the score
        max_eval = float('-inf')     # init at -inf
        best_move = None
        for move in get_all_moves(position, WHITE, game):   # for every possible move
            evaluation = minimax(move, depth-1, False, game, evaluate_function)[0]    # next = min
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move

    else:   # min the score
        min_eval = float('inf')  # init at inf for minimizing
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game, evaluate_function)[0]  # next = max
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, colour, game):  # check all moves of all the pieces
    moves = []
    for piece in board.get_all_pieces(colour):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)  # show the analysis of the AI
            temp_board = deepcopy(board)    # copy to not modify original board
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    return moves


def draw_moves(game, board, piece):     # follow machine analysis
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, GREEN, (piece.x, piece.y), 50, 5)
    game.draw_valid_moves((valid_moves.keys()))
    pygame.display.update()
    # pygame.time.delay(50)    # to show pieces analysis by machine slower - 100

