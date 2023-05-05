import pygame
import algorithme


class Tile:
    def __init__(self, x, y, value, init_value, notes, valid, window, size):
        self.x = x
        self.y = y
        self.value = value
        self.init_value = init_value
        self.notes = notes
        self.valid = valid
        self.window = window
        self.size = size
        self.rect = pygame.Rect(y, x, self.size, self.size)
        self.background_color = "white"
        self.selected = False

    def draw(self):
        surface: pygame.Surface = self.window.subsurface(self.rect)
        surface.fill(self.background_color)
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

    def display(self):
        if self.value != "0":
            font = pygame.font.SysFont("arial", 50)
            color = "red"
            if self.init_value == "0" and self.valid:
                color = "blue"
            elif self.init_value != "0":
                color = "black"
            text = font.render(self.value, True, color)
            self.window.blit(text, text.get_rect(center=self.rect.center))
        elif len(self.notes) > 0:
            font = pygame.font.SysFont("arial", 15)
            for i in range(len(self.notes)):
                pos = (
                    self.y
                    + 10
                    + 20 * ((algorithme.get_character_index(self.notes[i]) - 1) % 3),
                    self.x
                    + 10
                    + 20 * ((algorithme.get_character_index(self.notes[i]) - 1) // 3),
                )
                text = font.render(self.notes[i], True, (0, 0, 0))
                self.window.blit(text, text.get_rect(center=pos))

    def get_pos(self):
        return self.x // self.size, self.y // self.size
