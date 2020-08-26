"""
Main driver file.
Responsible for handling user input and displaying the current GameState object
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {}


def draw_board(screen):
    """
    Draws the squares on the board
    """
    # list of colors for chess board
    colors = [p.Color("tan"), p.Color("beige")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draws the pieces on the board using the current gs.board
    Separate from draw_board for Highlighting purposes
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece!= "--":  # check to make sure it's not an empty square
                screen.blit(IMAGES[piece],p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
    """
    Responsible for all graphics in the current game state
    """
    draw_board(screen)  # draws the squares
    # TODO: add in piece highlighting and move suggestions
    draw_pieces(screen, gs.board)  # draws pieces on top of squares


def load_images():
    """
    Initialize global dictionary of images(pieces).
    Only called once.
    """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """
    Main driver.
    Handles user input and updating the board
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
