from board import Board
import pygame
import os

board = pygame.image.load(os.path.join("img","board.png"))
board = pygame.transform.scale(board, (750, 750))


def redraw_game_window():
    global window
    window.blit(board, (0, 0))
    game_board = Board(8, 8, window)
    game_board.draw_board()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(10)

        redraw_game_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass


width = 750
height = 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
main()

