from piece import Bishop
from piece import King
from piece import Knight
from piece import Pawn
from piece import Queen
from piece import Rook


class Board(object):
    def __init__(self, rows, cols, window):
        self.rows = rows
        self.cols = cols
        self.window = window

    def draw_board(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if y == 0 or y == 7:
                    if x == 0:
                        b_rook = Rook(x, y, 1)
                        b_rook.initial_draw(self.window)
                    if x == 7:
                        w_rook = Rook(x, y, 0)
                        w_rook.initial_draw(self.window)
                if y == 1 or y == 6:
                    if x == 0:
                        b_knight = Knight(x, y, 1)
                        b_knight.initial_draw(self.window)
                    if x == 7:
                        w_knight = Knight(x, y, 0)
                        w_knight.initial_draw(self.window)
                if y == 2 or y == 5:
                    if x == 0:
                        b_bishop = Bishop(x, y, 1)
                        b_bishop.initial_draw(self.window)
                    if x == 7:
                        w_bishop = Bishop(x, y, 0)
                        w_bishop.initial_draw(self.window)
                if y == 3:
                    if x == 0:
                        b_king = King(x, y, 1)
                        b_king.initial_draw(self.window)
                    if x == 7:
                        w_king = King(x, y, 0)
                        w_king.initial_draw(self.window)
                if y == 4:
                    if x == 0:
                        b_queen = Queen(x, y, 1)
                        b_queen.initial_draw(self.window)
                    if x == 7:
                        w_queen = Queen(x, y, 0)
                        w_queen.initial_draw(self.window)
                if x == 1:
                    b_pawn = Pawn(x, y, 1)
                    b_pawn.initial_draw(self.window)
                if x == 6:
                    w_pawn = Pawn(x, y, 0)
                    w_pawn.initial_draw(self.window)
