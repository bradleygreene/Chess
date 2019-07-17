import pygame
import os

white_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
white_king = pygame.image.load(os.path.join("img", "white_king.png"))
white_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
white_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
white_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
white_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

black_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
black_king = pygame.image.load(os.path.join("img", "black_king.png"))
black_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
black_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
black_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
black_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w = [white_bishop, white_king, white_knight, white_pawn, white_queen, white_rook]
b = [black_bishop, black_king, black_knight, black_pawn, black_queen, black_rook]

white = []
black = []

for img in w:
    white.append(pygame.transform.scale(img, (93, 93)))

for img in b:
    black.append(pygame.transform.scale(img, (93, 93)))


class Piece(object):
    img = -1

    def __init__(self, initial_row, initial_col, player_number):
        self.valid_moves = {}
        self.initial_row = initial_row
        self.initial_col = initial_col
        self.location = [0, 0]
        self.player = player_number
        self.selected = False

    def initial_draw(self, window):
        """
        The initial location of each piece
        (From the piece perspective, it is (0,0))
        """
        if self.player == 1:
            draw = black[self.img]
        else:
            draw = white[self.img]

        x = round(self.initial_col * (750 / 8))
        y = round(self.initial_row * (750 / 8))

        window.blit(draw, (x, y))

    def move(self, row, col):
        """
        Move piece to location
        :param row: Current row
        :param col: Current column
        :return: new location
        """

    def is_selected(self):
        """

        :return: Returns if the piece is selected
        """
        return True

    def valid_move(self, row, col):
        """
        Checks to see if the location given is valid
        :param row:
        :param col:
        :return: True if same color piece isn't there and if that piece can move in that direction. Else false
        """

        return True


class Bishop(Piece):
    img = 0


class King(Piece):
    img = 1


class Knight(Piece):
    img = 2


class Pawn(Piece):
    img = 3


class Queen(Piece):
    img = 4


class Rook(Piece):
    img = 5
