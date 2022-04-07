import pygame
from .constants import BLACK, ROWS, SQUARE_SIZE, COLS, WHITE, GREY
from .piece import Piece


def draw_squares(win):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def subs(white_evaluation, black_evaluation, colour):

    if colour == WHITE:
        return white_evaluation - black_evaluation
    elif colour == BLACK:
        return black_evaluation - white_evaluation

    return 0


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 20
        self.black_kings = self.white_kings = 0
        self.create_board()

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if not piece.king:
                piece.make_king()
                if piece.colour == WHITE:
                    self.white_kings += 1
                else:
                    self.black_kings += 1

    # Evaluation functions: evaluate the current state of the board

    def evaluate_function_1(self, colour):  # Piece to value
        # score based on the number of pieces left
        white_evaluation = self.white_left + self.white_kings * 2
        if self.winner() is WHITE:
            white_evaluation += 250
        black_evaluation = self.black_left + self.black_kings * 2
        if self.winner() is WHITE:
            black_evaluation += 250

        return subs(colour, white_evaluation, black_evaluation)

    def evaluate_function_2(self, colour):
        # Pawn in the opponent's half of the board value = 7
        # Pawn in the player's half of the board value = 5
        # King value = 10
        # win = 250

        white_evaluation = black_evaluation = 0
        white_pieces = self.get_all_pieces(WHITE)
        black_pieces = self.get_all_pieces(BLACK)
        first_board_half = []
        second_board_half = []

        for row in range(int(ROWS/2)):
            first_board_half.append(row)
            second_board_half.append(row+5)

        for white_piece in white_pieces:
            aux = 0
            if self.winner() is WHITE:
                aux += 250

            if white_piece.king:    # if king
                aux += 10
            else:
                if white_piece.row in first_board_half:     # white pawn in white player part
                    aux += 5
                else:   # white pawn in black player's part (more value)
                    aux += 7

            white_evaluation += aux

        for black_piece in black_pieces:
            aux = 0
            if self.winner() is BLACK:
                aux += 250

            if black_piece.king:  # if king
                aux += 10
            else:
                if black_piece.row in second_board_half:  # black pawn in black player part
                    aux += 5
                else:   # black pawn in white player's part (more value)
                    aux += 7

            black_evaluation += aux

        return subs(white_evaluation, black_evaluation, colour)

    def get_all_pieces(self, colour):
        pieces = []

        for row in self.board:
            for piece in row:
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)

        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.black_left <= 0:    # no more black pawns -> white = winner
            return WHITE
        elif self.white_left <= 0:
            return BLACK

        # check if draw -> no more movements possible
        white_pieces = self.get_all_pieces(WHITE)
        black_pieces = self.get_all_pieces(BLACK)
        white_can_move = False
        black_can_move = False

        # check if none of the players can move
        for white_piece in white_pieces:
            if self.get_valid_moves(white_piece):
                white_can_move = True    # draw will be represented with color GREY
                break

        for black_pieces in black_pieces:
            if self.get_valid_moves(black_pieces):
                black_can_move = True
                break

        if not white_can_move or not black_can_move:
            # return GREY  # draw will be represented with color GREY
            # no more draw, only win option depending on the number of pawns left (if same -> draw)
            if self.white_left < self.black_left:
                return BLACK
            elif self.white_left > self.black_left:
                return WHITE
            else:
                return GREY

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.colour == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.colour, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.colour, right))
        if piece.colour == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.colour, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.colour, right))

        return moves

    def _traverse_left(self, start, stop, step, colour, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, colour, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, colour, left + 1, skipped=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, colour, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, colour, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, colour, right + 1, skipped=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]

            right += 1

        return moves
