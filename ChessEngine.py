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
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()  # square coordinates where en passant is possible
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wKs, self.current_castling_rights.bKs, 
                                               self.current_castling_rights.wQs, self.current_castling_rights.bQs)]

    def make_move(self, move):
        """
        Takes a move and executes it (does not work for castling, pawn promotion, and en-passant)
        """
        self.board[move.start_row][move.start_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move) 
        self.white_to_move = not self.white_to_move  # switching turns
        # update king's location if moved
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_column)
        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_column] = move.piece_moved[0] + 'Q'
        # en passant 
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_column] = "--"  # capturing the pawn
        # update enpassant_possible 
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row)//2, move.end_column)
        else:
            self.enpassant_possible = ()
        # castling
        if move.is_castle_move:
            if move.end_column - move.start_column == 2:  # king side caslte
                self.board[move.end_row][move.end_column-1] = self.board[move.end_row][move.end_column+1]
                self.board[move.end_row][move.end_column+1] = "--"
            else:  # queen side castle
                self.board[move.end_row][move.end_column+1] = self.board[move.end_row][move.end_column-2]
                self.board[move.end_row][move.end_column-2] = "--"
        # update castling rights
        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wKs, self.current_castling_rights.bKs, 
                                                   self.current_castling_rights.wQs, self.current_castling_rights.bQs))

    def undo_move(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move  # switching turns
            # update king's location if moved
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_column)
            # undo en passant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_column] = "--"  # leave landing square blank
                self.board[move.start_row][move.end_column] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_column)
            # undo a 2 square pawn advance
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()
            # undo castling rights
            self.castle_rights_log.pop()
            new_rights = self.castle_rights_log[-1]
            self.current_castling_rights = CastleRights(new_rights.wKs, new_rights.bKs, new_rights.wQs, new_rights.bQs)
            # undo castle move
            if move.is_castle_move:
                if move.end_column - move.start_column == 2:  # king side
                    self.board[move.end_row][move.end_column+1] = self.board[move.end_row][move.end_column-1]
                    self.board[move.end_row][move.end_column-1] = "--"
                else:  # queen side
                    self.board[move.end_row][move.end_column-2] = self.board[move.end_row][move.end_column+1]
                    self.board[move.end_row][move.end_column+1] = "--"

    def update_castle_rights(self, move):
        """
        Update the castle rights given the move
        """
        if move.piece_moved == "wK":
            self.current_castling_rights.wKs = False
            self.current_castling_rights.wQs = False
        elif move.piece_moved == "bK":
            self.current_castling_rights.bKs = False
            self.current_castling_rights.bQs = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_column == 0:  # left rook
                    self.current_castling_rights.wQs = False
                elif move.start_column == 7:  # right rook
                    self.current_castling_rights.wKs = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_column == 0:  # left rook
                    self.current_castling_rights.bQs = False
                elif move.start_column == 7:  # right rook
                    self.current_castling_rights.bKs = False
    
    def get_valid_moves(self):
        """
        Gets all valid moves from current player, makes move for each possible move,
        generates all possible moves again (for opponent), checks if king can be attacked
        If king is safe -> valid move

        :return: list of valid moves only
        """
        for log in self.castle_rights_log:
            print(log.wKs, log.wQs, log.bKs, log.bQs, end=", ")
        print()
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = CastleRights(self.current_castling_rights.wKs, self.current_castling_rights.bKs,
                                          self.current_castling_rights.wQs, self.current_castling_rights.bQs)
        moves = self.get_all_possible_moves()
        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)
        for i in range(len(moves)-1, -1, -1):  # when removing from list, going backwards
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])  # king is not safe, not valid move
            self.white_to_move = not self.white_to_move
            self.undo_move() 
        if len(moves) == 0:  # either checkmate or stalemate
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        
        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castle_rights

        return moves

    def in_check(self):
        """
        Determine if current player is in check
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, column):
        """
        Determine if enemy can attack the square row, column
        """
        self.white_to_move = not self.white_to_move  # switch to opponents turn
        opponents_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move  # switch turns back
        for move in opponents_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False

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
                elif (row-1, column-1) == self.enpassant_possible:  # en passant handling
                    moves.append(Move((row, column), (row-1, column-1), self.board, is_enpassant_move=True))
            if column+1 <= 7:  # captures to the right
                if self.board[row-1][column+1][0] == "b":  # enemy piece to capture
                    moves.append(Move((row, column), (row-1, column+1), self.board))
                elif (row-1, column+1) == self.enpassant_possible:  # en passant handling
                    moves.append(Move((row, column), (row-1, column+1), self.board, is_enpassant_move=True))
        else:  # black pawn
            if self.board[row+1][column] == "--":  # 1 square pawn advance
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 1 and self.board[row+2][column] == "--":  # 2 square pawn advance
                    moves.append(Move((row, column), (row+2, column), self.board))
            if column-1 >= 0:  # captures to the left
                if self.board[row+1][column-1][0] == "w":  # enemy piece to capture
                    moves.append(Move((row, column), (row+1, column-1), self.board))
                elif (row+1, column-1) == self.enpassant_possible:  # en passant handling
                    moves.append(Move((row, column), (row+1, column-1), self.board, is_enpassant_move=True))
            if column+1 <= 7:  # captures to the right
                if self.board[row+1][column+1][0] == "w":  # enemy piece to capture
                    moves.append(Move((row, column), (row+1, column+1), self.board))
                elif (row+1, column+1) == self.enpassant_possible:  # en passant handling
                    moves.append(Move((row, column), (row+1, column+1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, column, moves):
        """
        Get all the rook moves for the rook located in row, column, and add these moves to the list
        :return: Returns a list of all possible moves for the rook
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
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

    def get_castle_moves(self, row, column, moves):
        """
        Generate all valid castle moves for the king at (row, column) and add them to the list of moves
        """
        if self.square_under_attack(row, column):
            return  # can't castle while in check
        if (self.white_to_move and self.current_castling_rights.wKs) or \
                (not self.white_to_move and self.current_castling_rights.bKs):
            self.get_Ks_castle_moves(row, column, moves)
        if (self.white_to_move and self.current_castling_rights.wQs) or \
                (not self.white_to_move and self.current_castling_rights.bQs):
            self.get_Qs_castle_moves(row, column, moves)
    
    def get_Ks_castle_moves(self, row, column, moves):
        """
        Checks if square are empty in between king and rook (king side)
        Adds the castle move to list of moves
        """
        if self.board[row][column+1] == "--" and self.board[row][column+2] == "--":
            if not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column+2):
                moves.append(Move((row, column), (row, column+2), self.board, is_castle_move=True))
    
    def get_Qs_castle_moves(self, row, column, moves):
        """
        Checks if square are empty in between king and rook (queen side)
        Adds the castle move to list of moves
        """
        if self.board[row][column-1] == "--" and self.board[row][column-2] == "--" and self.board[row][column-3]:
            if not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column-2):
                moves.append(Move((row, column), (row, column-2), self.board, is_castle_move=True))


class CastleRights():
    """
    This class stores the current state of our castling rights
    One for each side of both kings
    """
    def __init__(self, wK_side, bK_side, wQ_side, bQ_side):
        self.wKs = wK_side
        self.bKs = bK_side
        self.wQs = wQ_side
        self.bQs = bQ_side


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

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.is_pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or \
                                 (self.piece_moved == "bP" and self.end_row == 7)
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"
        self.is_castle_move = is_castle_move
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
