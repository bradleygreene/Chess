class GameState:
    """
    This class is responsible for storing all information about the current state of a chess game.
    Responsible for determing valid moves at the current state.
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
