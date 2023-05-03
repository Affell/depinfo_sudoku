from board import Board
import numpy as np
import pygame


def main():
    matrix: np.ndarray = prompt_starting_position()
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    board: Board = Board(screen, matrix)
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

        clock.tick(60)

    pygame.quit()


def prompt_starting_position() -> np.ndarray:
    return np.array(
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
    )
    matrix: np.ndarray = np.zeros((9, 9), dtype=np.intp)
    print("Saisissez la grille de départ : ")
    for i in range(9):
        line: str = input()
        if len(line) != 9:
            print(
                "Entrez 9 caractères sur 9 lignes correspondants à la grille de départ"
            )
            return prompt_starting_position()
        for j in range(9):
            try:
                nb = int(line[j])
                matrix[i][j] = nb
            except ValueError as _:
                if line[j] != " ":
                    print("Caractère invalide")
                    return prompt_starting_position()
    return matrix


if __name__ == "__main__":
    main()
