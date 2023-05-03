import pygame


class Tile:
    def __init__(self, value, window, x, y):
        self.value = value
        self.width = 60
        self.height = 60
        self.window = window
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.background_color = "white"
        self.selected = False

    def draw(self):
        surface: pygame.Surface = self.window.subsurface(self.rect)
        surface.fill(self.background_color)
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

    def display(self):
        if self.value != 0:
            font = pygame.font.SysFont("arial", 50)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.window.blit(text, text.get_rect(center=self.rect.center))

    def get_pos(self):
        return self.y // 60, self.x // 60
