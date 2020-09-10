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
    colors = [p.Color("beige"), p.Color("tan")]
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
            if piece != "--":  # check to make sure it's not an empty square
                screen.blit(IMAGES[piece], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


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
    valid_moves = gs.get_valid_moves()
    move_made = False  # Flag variable for when a move is made
    load_images()
    running = True
    square_selected = ()  # no square selected initially, keeps track of the last user click
    player_clicks = []  # keeps track of player clicks [(1,2),(2,2)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if square_selected == (row, column):  # checking if user clicks the same square twice
                    square_selected = ()  # deselects
                    player_clicks = []  # clear player clicks
                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            # reset user clicks
                            square_selected = ()
                            player_clicks = []
                    if not move_made:
                        player_clicks = [square_selected]

            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
