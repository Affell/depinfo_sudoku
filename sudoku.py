from board import Board
from button import Button
import algorithme
import numpy as np
import pygame


def main():
    matrix: np.ndarray = algorithme.lecture_grille()
    solution: np.ndarray = algorithme.resoud_grille(matrix)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    board: Board = Board(screen, matrix, solution)

    def on_click():
        board.note = not board.note

    note_button: Button = Button(1000, 90, screen, 150, 150, "Note", on_click)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                try:
                    board.enter_digit(int(event.unicode))
                except ValueError as _:
                    pass
        if pygame.mouse.get_pressed() == (1, 0, 0):
            tile = board.get_tile(*pygame.mouse.get_pos())
            if tile is not None:
                board.select_tile(tile)

        screen.fill("white")
        board.draw_board()
        note_button.process(board)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
