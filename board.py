import numpy as np
import pygame
from tile import Tile
import algorithme


class Board:
    def __init__(
        self,
        name: str,
        screen: pygame.Surface,
        matrix: np.ndarray,
        progress: np.ndarray,
        notes: np.ndarray,
        noteMode,
        errors: int,
        solution: np.ndarray,
    ):
        self.name = name
        self.init_board = np.array(matrix)
        self.size = self.init_board.shape[0]
        self.error_count = errors
        self.solution = np.array(solution)
        self.window = screen.subsurface(pygame.Rect(340, 90, 540, 540))
        self.tiles = [
            [
                Tile(
                    i * (540 // self.size),
                    j * (540 // self.size),
                    progress[i][j],
                    self.init_board[i][j],
                    notes[i][j] if len(notes) > 0 else [],
                    self.solution[i][j] == progress[i][j],
                    self.window,
                    540 // self.size,
                )
                for j in range(self.size)
            ]
            for i in range(self.size)
        ]
        self.noteMode = noteMode
        self.error_rect = screen.subsurface(pygame.Rect(950, 50, 200, 30))

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[i][j].draw()
                self.tiles[i][j].display()
        for i in range(1, int(self.size**0.5) + 1):
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (i * (540 // self.size) * self.size**0.5, 0),
                (i * (540 // self.size) * self.size**0.5, 540),
                5,
            )
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (0, i * (540 // self.size) * self.size**0.5),
                (540, i * (540 // self.size) * self.size**0.5),
                5,
            )

        font = pygame.font.SysFont("arial", 20)
        text = font.render(f"erreurs : {self.error_count}", True, "black")
        self.error_rect.blit(
            text, text.get_rect(center=self.error_rect.get_rect().center)
        )

    def get_tile(self, x, y) -> Tile:
        x -= 340
        y -= 90
        if 0 <= x < 540 and 0 <= y < 540:
            return self.tiles[y // (540 // self.size)][x // (540 // self.size)]
        return None

    def select_tile(self, tile: Tile):
        pos = tile.get_pos()
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[i][j].selected = False
                if (self.tiles[i][j].value != "0" or (i, j) == pos) and self.tiles[i][
                    j
                ].value == tile.value:
                    self.tiles[i][j].background_color = "green"
                elif (
                    i == pos[0]
                    or j == pos[1]
                    or (i // self.size**0.5, j // self.size**0.5)
                    == (pos[0] // self.size**0.5, pos[1] // self.size**0.5)
                ):
                    self.tiles[i][j].background_color = "gray"
                else:
                    self.tiles[i][j].background_color = "white"
        tile.selected = True

    def enter_char(self, char: str):
        if char not in algorithme.get_allowed_characters(self.size):
            return
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j].selected and self.init_board[i][j] == "0":
                    if self.noteMode:
                        if char != "0":
                            self.tiles[i][j].value = "0"
                            if char in self.tiles[i][j].notes:
                                self.tiles[i][j].notes.remove(char)
                            else:
                                self.tiles[i][j].notes.append(char)
                    else:
                        self.tiles[i][j].notes.clear()
                        self.tiles[i][j].value = char
                        if self.solution[i][j] == char:
                            self.tiles[i][j].valid = True
                        else:
                            self.tiles[i][j].valid = False
                            self.error_count += 1 if char != "0" else 0
                        self.select_tile(self.tiles[i][j])
                    break

    def save(self):
        with open(f"./grids/{self.name}.sudoku", "w") as f:
            f.writelines(
                [",".join([e for e in line]) + "\n" for line in self.init_board]
            )
            f.write(f"PROGRESS:{self.error_count}\n")
            f.writelines(
                [",".join([tile.value for tile in line]) + "\n" for line in self.tiles]
            )
            f.write(f"NOTES:{self.noteMode}\n")
            f.writelines(
                [
                    ",".join(["|".join([note for note in tile.notes]) for tile in line])
                    + "\n"
                    for line in self.tiles
                ]
            )
