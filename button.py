import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        window,
        width,
        height,
        fontColor,
        buttonText="Button",
        onclickFunction=None,
        onePress=False,
        image=False,
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
        self.fontColor = fontColor
        self.image = pygame.image.load(image)

    def process(self):
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
        text = self.font.render(self.buttonText, True, self.fontColor)
        self.window.blit(
            text,
            text.get_rect(
                center=(self.buttonRect.center[0], self.y + self.height - 20)
            ),
        )
        self.window.blit(self.image, (self.buttonRect.center[0] - 32, self.y))
