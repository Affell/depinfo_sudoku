import numpy as np
import pygame
from tile import Tile


class Board:
    def __init__(self, window: pygame.Surface, matrix):
        self.init_board = np.array(
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
        self.board = np.array(self.init_board)
        self.window = window.subsurface(pygame.Rect(340, 90, 540, 540))
        self.tiles = [
            [Tile(self.board[i][j], self.window, i * 60, j * 60) for i in range(9)]
            for j in range(9)
        ]

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw()
                self.tiles[i][j].display()
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (((j // 3) * 180) + 1, 0),
                        (((j // 3) * 180) + 1, 540),
                        5,
                    )

                if i % 3 == 0 and i != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (0, ((i // 3) * 180) + 1),
                        (540, ((i // 3) * 180) + 1),
                        5,
                    )

        pygame.display.flip()
        pygame.display.update()

    def get_tile(self, x, y) -> Tile:
        x -= 340
        y -= 90
        if 0 <= x < 540 and 0 <= y < 540:
            return self.tiles[y // 60][x // 60]
        return None

    def select_tile(self, tile: Tile):
        pos = tile.get_pos()
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].selected = False
                if self.tiles[i][j].value == tile.value:
                    self.tiles[i][j].background_color = "green"
                elif (
                    i == pos[0]
                    or j == pos[1]
                    or (i // 3, j // 3) == (pos[0] // 3, pos[1] // 3)
                ):
                    self.tiles[i][j].background_color = "gray"
                else:
                    self.tiles[i][j].background_color = "white"
        tile.selected = True

    def enter_digit(self, nb: int):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].selected and self.init_board[i][j] == 0:
                    self.tiles[i][j].value = nb
