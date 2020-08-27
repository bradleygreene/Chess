class GameState:
    """
    This class is responsible for storing all information about the current state of a chess game.
    Responsible for determining valid moves at the current state.
    Also keeps a move log.
    """
    def __init__(self):

        # board is an 8x8 2d list, with each element containing 2 characters
        # first character is the color of the piece (black or white)
        # second is the piece (Rook(R), Knight(N), Bishop(B), Queen(Q), King(K), or Pawn(P))
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []
     
    def make_move(self, move):
        """
        Takes a move and executes it (does not work for castling, pawn promotion, and en-passant)
        """
        self.board[move.start_row][move.start_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move) 
        self.white_to_move = not self.white_to_move  # switching turns

    def undo_move(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move  # switcing turns


class Move:
    """
    This class represents the moves made on a chess board.
    It gets the information needed for a move to be made.
    """
    # mapping keys from the board as if the player would see it, not a computer
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                     "5": 3, "6": 2, "7": 1, "8": 0}
    row_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, 
                        "e": 4, "f": 5, "g": 6, "h": 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + \
            self.get_rank_file(self.end_row, self.end_column)
    
    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.row_to_ranks[row]
