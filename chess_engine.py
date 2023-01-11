"""
Game state & valid moves & moves log
"""


def isonboard(pos):
    if pos[0] in range(8) and pos[1] in range(8):
        return True
    return False


class GameState:
    piece_values = {"P" : 1, "R" : 5, "N":3, "B": 3, "Q" : 9, "K":0}
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []
        self.material_delta = self.count_material_delta()
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.winner = ''
    def count_material_delta(self):
        material = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c][0] == "w":
                    material += self.piece_values[self.board[r][c][1]]
                if self.board[r][c][0] == "b":
                    material -= self.piece_values[self.board[r][c][1]]
        return material
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        if move.piece_moved == 'wK':
            self.white_king_pos = (move.end_row, move.end_col)
        if move.piece_moved == 'bK':
            self.black_king_pos = (move.end_row, move.end_col)
        self.white_to_move = not self.white_to_move

    def checkmate_stalemate(self):
        if self.get_valid_moves(self.get_all_possible_moves()) == []:
            if self.in_check():
                self.checkmate = True
                self.winner = 'b' if self.white_to_move else 'w'
            else:
                self.stalemate = True
                self.winner = 'd'
    def resign(self):

        self.winner = "b" if self.white_to_move else "w"
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop(-1)
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_pos = (move.start_row, move.start_col)
            if move.piece_moved == 'bK':
                self.black_king_pos = (move.start_row, move.start_col)
            self.checkmate = False
            self.stalemate = False

    def get_valid_moves(self, moves):
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        return moves
    def get_piece_moves(self, r, c):
        moves = []
        turn = self.board[r][c][0]
        if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
            piece = self.board[r][c][1]
            if piece == 'P':
                moves = self.get_pawn_moves(r, c)
            if piece == 'R':
                moves = self.get_rook_moves(r, c)
            if piece == 'B':
                moves = self.get_bishop_moves(r, c)
            if piece == 'Q':
                moves = self.get_queen_moves(r, c)
            if piece == 'N':
                moves = self.get_knight_moves(r, c)
            if piece == 'K':
                moves = self.get_king_moves(r, c)
        return moves

    def get_all_possible_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                moves.extend(self.get_piece_moves(r, c))
        return moves

    def get_pawn_moves(self, r, c):
        moves = []
        if self.white_to_move and self.board[r][c][0] == 'w':
            if self.board[r-1][c] == "--":
                moves.append(Move([r,c], [r-1, c], self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move([r, c], [r-2, c], self.board))
            if c > 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move([r, c], [r-1, c-1], self.board))
            if c < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move([r, c], [r-1, c+1], self.board))
        if not self.white_to_move and self.board[r][c][0] == 'b':
            if self.board[r+1][c] == "--":
                moves.append(Move([r,c], [r+1, c], self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move([r, c], [r+2, c], self.board))
            if c > 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move([r, c], [r+1, c-1], self.board))
            if c < 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move([r, c], [r+1, c+1], self.board))
        return moves
    def get_rook_moves(self, r, c):
        moves = []
        color = self.board[r][c][0]
        opponent = 'b' if color == 'w' else 'w'
        directions = [[0, 1], [0, -1], [-1, 0], [1, 0]]
        for dir in directions:
            row = r + dir[0]
            col = c + dir[1]
            while isonboard([row, col]):
                if self.board[row][col] == "--":
                    moves.append(Move([r,c], [row, col], self.board))
                    row = row + dir[0]
                    col = col + dir[1]

                elif self.board[row][col][0] == opponent:
                    moves.append(Move([r,c], [row, col], self.board))
                    break
                else:
                    break
        return moves
    def get_bishop_moves(self, r, c):
        moves = []
        color = self.board[r][c][0]
        opponent = 'b' if color == 'w' else 'w'
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for dir in directions:
            row = r + dir[0]
            col = c + dir[1]
            while isonboard([row, col]):
                if self.board[row][col] == "--":
                    moves.append(Move([r, c], [row, col], self.board))
                    row = row + dir[0]
                    col = col + dir[1]

                elif self.board[row][col][0] == opponent:
                    moves.append(Move([r, c], [row, col], self.board))
                    break
                else:
                    break
        return moves
    def get_queen_moves(self, r, c):
        moves = []
        color = self.board[r][c][0]
        opponent = 'b' if color == 'w' else 'w'
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, 1], [0, -1], [-1, 0], [1, 0]]
        for dir in directions:
            row = r + dir[0]
            col = c + dir[1]
            while isonboard([row, col]):
                if self.board[row][col] == "--":
                    moves.append(Move([r, c], [row, col], self.board))
                    row = row + dir[0]
                    col = col + dir[1]

                elif self.board[row][col][0] == opponent:
                    moves.append(Move([r, c], [row, col], self.board))
                    break
                else:
                    break
        return moves
    def get_knight_moves(self, r, c):
        moves = []
        color = self.board[r][c][0]
        directions = [[2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1], [1, -2], [1, 2]]
        for dir in directions:
            row = r + dir[0]
            col = c + dir[1]
            if isonboard([row, col]) and self.board[row][col][0] != color:
                moves.append(Move([r, c], [row, col], self.board))
        return moves
    def get_king_moves(self, r, c):
        moves = []
        color = self.board[r][c][0]
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, 1], [0, -1], [-1, 0], [1, 0]]
        for dir in directions:
            row = r + dir[0]
            col = c + dir[1]
            if isonboard([row, col]) and self.board[row][col][0] != color:
                moves.append(Move([r, c], [row, col], self.board))

        for move in self.move_log:
            if [move.start_row, move.start_col] == [7, 4]:
                pass

        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_pos[0], self.white_king_pos[1])
        else:
            return self.square_under_attack(self.black_king_pos[0], self.black_king_pos[1])

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.board = board
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = 1000 * self.start_row + 100 * self.start_col + 10 * self.end_row + self.end_col
        self.notation = self.get_notation()

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def get_notation(self):
        notation = ''
        if self.piece_moved[1] != "P":
            notation += self.piece_moved[1]
        if self.piece_moved[1] == "P" and self.piece_captured != "--":
            notation += f'{self.cols_to_files[self.start_col]}x'
        elif self.piece_captured != "--":
            notation += 'x'
        notation += self.get_rank_file(self.end_row, self.end_col)
        return notation

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
