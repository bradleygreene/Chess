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
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
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
            self.white_to_move = not self.white_to_move  # switching turns
    
    def get_valid_moves(self):
        """
        Gets all valid moves from all possible moves.
        Makes move, generates all possible moves again, checks if king can be attacked
        If king is safe -> valid move
        :return: list of valid moves only
        """
        return self.get_all_possible_moves()  # TODO: actually check valid moves

    def get_all_possible_moves(self):
        """
        Gets all possible moves for the current player
        :return: list of all moves
        """
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][column][1]
                    self.move_functions[piece](row, column, moves)  # calls the appropriate move functions
        return moves

    def get_pawn_moves(self, row, column, moves):
        """
        Get all the pawn moves for the pawn located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the pawn
        """
        if self.white_to_move:  # white pawn moves
            if self.board[row-1][column] == "--":  # 1 square pawn advance
                moves.append(Move((row, column), (row-1, column), self.board))
                if row == 6 and self.board[row-2][column] == "--":  # 2 square pawn advance
                    moves.append(Move((row, column), (row-2, column), self.board))
            if column-1 >= 0:  # captures to the left
                if self.board[row-1][column-1][0] == "b":  # enemy piece to capture
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            if column+1 <= 7:  # captures to the right
                if self.board[row-1][column+1][0] == "b":  # enemy piece to capture
                    moves.append(Move((row, column), (row-1, column+1), self.board))

        else:  # black pawn
            if self.board[row+1][column] == "--":  # 1 square pawn advance
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 1 and self.board[row+2][column] == "--":  # 2 square pawn advance
                    moves.append(Move((row, column), (row+2, column), self.board))
            if column-1 >= 0:  # captures to the left
                if self.board[row+1][column-1][0] == "w":  # enemy piece to capture
                    moves.append(Move((row, column), (row+1, column-1), self.board))
            if column+1 <= 7:  # captures to the right
                if self.board[row+1][column+1][0] == "w":  # enemy piece to capture
                    moves.append(Move((row, column), (row+1, column+1), self.board))

    def get_rook_moves(self, row, column, moves):
        """
        Get all the rook moves for the rook located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the rook
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = row + d[0] * i
                end_column = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "--":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off the board
                    break

    def get_knight_moves(self, row, column, moves):
        """
        Get all the knight moves for the knight located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the knight
        """
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        friendly_color = "w" if self.white_to_move else "b"
        for n in knight_moves:
            end_row = row + n[0]
            end_column = column + n[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0] != friendly_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row, column, moves):
        """
        Get all the bishop moves for the bishop located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the bishop
        """
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # for directions
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_column = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "--":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off the board
                    break

    def get_king_moves(self, row, column, moves):
        """
        Get all the king moves for the king located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the king
        """
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        friendly_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_column = column + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0] != friendly_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_queen_moves(self, row, column, moves):
        """
        Get all the queen moves for the queen located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the queen
        """
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)


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
        self.move_ID = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        """
        Overriding the equal method
        """
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + \
            self.get_rank_file(self.end_row, self.end_column)
    
    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.row_to_ranks[row]
