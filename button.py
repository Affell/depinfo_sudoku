import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        window,
        width,
        height,
        buttonText="Button",
        onclickFunction=None,
        onePress=False,
    ):
        self.x = x
        self.y = y
        self.window = window
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface = window.subsurface(self.buttonRect)

        self.font = pygame.font.SysFont("Arial", 40)

    def process(self, board):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors["normal"])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors["pressed"])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        text = self.font.render(self.buttonText, True, "green" if board.note else "red")
        self.window.blit(
            text,
            text.get_rect(center=self.buttonRect.center),
        )
