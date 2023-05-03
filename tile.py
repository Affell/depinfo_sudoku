import pygame


class Tile:
    def __init__(self, x, y, value, window):
        self.x = x
        self.y = y
        self.value = value
        self.window = window
        self.width = 60
        self.height = 60
        self.rect = pygame.Rect(y, x, self.width, self.height)
        self.background_color = "white"
        self.selected = False
        self.notes = []

    def draw(self):
        surface: pygame.Surface = self.window.subsurface(self.rect)
        surface.fill(self.background_color)
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

    def display(self):
        if self.value != 0:
            font = pygame.font.SysFont("arial", 50)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.window.blit(text, text.get_rect(center=self.rect.center))
        elif len(self.notes) > 0:
            font = pygame.font.SysFont("arial", 15)
            for i in range(len(self.notes)):
                pos = (
                    self.y + 10 + 20 * ((self.notes[i] - 1) % 3),
                    self.x + 10 + 20 * ((self.notes[i] - 1) // 3),
                )
                text = font.render(str(self.notes[i]), True, (0, 0, 0))
                self.window.blit(text, text.get_rect(center=pos))

    def get_pos(self):
        return self.x // 60, self.y // 60
