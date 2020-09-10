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
    global colors
    colors = [p.Color("beige"), p.Color("tan")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animate_move(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    delta_row = move.end_row - move.start_row
    delta_column = move.end_column - move.start_column
    frames_per_square = 7
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square
    for frame in range(frame_count+1):
        row, column = (move.start_row + delta_row*frame/frame_count,
                       move.start_column + delta_column*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_column) % 2]
        end_sqaure = p.Rect(move.end_column*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_sqaure)
        # draw captured piece onto rectangle
        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_sqaure)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


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


def draw_game_state(screen, gs, valid_moves, square_selected):
    """
    Responsible for all graphics in the current game state
    """
    draw_board(screen)  # draws the squares
    highlight_squares(screen, gs, valid_moves, square_selected)
    draw_pieces(screen, gs.board)  # draws pieces on top of squares


def draw_text(screen, text):
    """
    Draws text on the screen
    """
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, p.Color("Red"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2,
                                                     HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    font = p.font.SysFont("Helvitca", 24, True, False)
    text_object = font.render("Press R to restart", 0, p.Color("Red"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                     HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location.move(0, 50))


def highlight_squares(screen, gs, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected
    """
    if square_selected != ():
        row, column = square_selected
        if gs.board[row][column][0] == ("w" if gs.white_to_move else "b"):  # square_selected is a piece that can move
            # highlight selected square
            surface = p.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)  # transparency value
            surface.fill(p.Color("black"))
            screen.blit(surface, (column*SQ_SIZE, row*SQ_SIZE))
            # highlight moves from that square
            surface.fill(p.Color("red"))
            for move in valid_moves:
                if move.start_row == row and move.start_column == column:
                    screen.blit(surface, (move.end_column*SQ_SIZE, move.end_row*SQ_SIZE))


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
    animate = False  # Flag variable for when to animate
    load_images()
    running = True
    square_selected = ()  # no square selected initially, keeps track of the last user click
    player_clicks = []  # keeps track of player clicks [(1,2),(2,2)]
    game_over = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
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
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                print(move.get_chess_notation())
                                move_made = True
                                animate = True
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
                    animate = False
                    game_over = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False
        draw_game_state(screen, gs, valid_moves, square_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif gs.stalemate:
            game_over = True
            draw_text(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
