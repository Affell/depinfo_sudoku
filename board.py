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
            [Tile(i * 60, j * 60, self.board[i][j], self.window) for j in range(9)]
            for i in range(9)
        ]
        self.note = True

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw()
                self.tiles[i][j].display()
        for i in range(1, 4):
            pygame.draw.line(self.window, (0, 0, 0), (i * 180, 0), (i * 180, 540), 5)
        for j in range(1, 4):
            pygame.draw.line(self.window, (0, 0, 0), (0, j * 180), (540, j * 180), 5)

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
                if (self.tiles[i][j].value != 0 or (i, j) == pos) and self.tiles[i][
                    j
                ].value == tile.value:
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
                    if self.note:
                        if nb > 0:
                            self.tiles[i][j].value = 0
                            if nb in self.tiles[i][j].notes:
                                self.tiles[i][j].notes.remove(nb)
                            else:
                                self.tiles[i][j].notes.append(nb)
                    else:
                        self.tiles[i][j].notes.clear()
                        self.tiles[i][j].value = nb
                        self.select_tile(self.tiles[i][j])
                    break
