import pygame
import algorithme


class Tile:
    def __init__(self, x, y, value, init_value, notes, valid, window, size, bloc_size):
        self.x = x
        self.y = y
        self.value = value
        self.init_value = init_value
        self.notes = notes
        self.valid = valid
        self.window = window
        self.size = size
        self.bloc_size = bloc_size
        self.rect = pygame.Rect(y, x, self.size, self.size)
        self.background_color = "white"
        self.selected = False

    def draw(self):
        surface: pygame.Surface = self.window.subsurface(self.rect)
        surface.fill(self.background_color)
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

    def display(self):
        if self.value != "0":
            font = pygame.font.SysFont("arial", 80 - 10 * self.bloc_size)
            color = "red"
            if self.init_value == "0" and self.valid:
                color = "blue"
            elif self.init_value != "0":
                color = "black"
            text = font.render(self.value, True, color)
            self.window.blit(text, text.get_rect(center=self.rect.center))
        elif len(self.notes) > 0:
            font = pygame.font.SysFont("arial", 24 - 3 * self.bloc_size)
            w, h = font.size(self.notes[0])
            for i in range(len(self.notes)):
                pos = (
                    self.y
                    + 1
                    + (self.size / self.bloc_size) // 2
                    + (self.size // self.bloc_size)
                    * (algorithme.get_character_index(self.notes[i]) % self.bloc_size),
                    self.x
                    + 1
                    + (self.size / self.bloc_size) // 2
                    + (self.size // self.bloc_size)
                    * (algorithme.get_character_index(self.notes[i]) // self.bloc_size),
                )
                text = font.render(self.notes[i], True, (0, 0, 0))
                self.window.blit(text, text.get_rect(center=pos))

    def get_pos(self):
        return self.x // self.size, self.y // self.size
