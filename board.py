import numpy as np
import pygame
from tile import Tile


class Board:
    def __init__(
        self,
        name: str,
        screen: pygame.Surface,
        matrix: np.ndarray,
        progress: np.ndarray,
        errors: int,
        solution: np.ndarray,
    ):
        self.name = name
        self.init_board = np.array(matrix)
        self.board = np.array(progress)
        self.error_count = errors
        self.solution = np.array(solution)
        self.window = screen.subsurface(pygame.Rect(340, 90, 540, 540))
        self.tiles = [
            [
                Tile(
                    i * 60, j * 60, self.board[i][j], self.init_board[i][j], self.window
                )
                for j in range(9)
            ]
            for i in range(9)
        ]
        self.note = False
        self.error_rect = screen.subsurface(pygame.Rect(950, 50, 200, 30))

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw()
                self.tiles[i][j].display()
        for i in range(1, 4):
            pygame.draw.line(self.window, (0, 0, 0), (i * 180, 0), (i * 180, 540), 5)
        for j in range(1, 4):
            pygame.draw.line(self.window, (0, 0, 0), (0, j * 180), (540, j * 180), 5)

        font = pygame.font.SysFont("arial", 20)
        text = font.render(f"erreurs : {self.error_count}", True, "black")
        self.error_rect.blit(
            text, text.get_rect(center=self.error_rect.get_rect().center)
        )

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
                        if self.solution[i][j] == nb:
                            self.tiles[i][j].valid = True
                        else:
                            self.tiles[i][j].valid = False
                            self.error_count += 1 if nb != 0 else 0
                        self.select_tile(self.tiles[i][j])
                    break

    def save(self):
        with open(f"./grids/{self.name}.sudoku", "w") as f:
            f.writelines([",".join([str(e) for e in line]) for line in self.init_board])
            f.write(f"PROGRESS:{self.error_count}")
            f.writelines([",".join([str(e) for e in line]) for line in self.board])
