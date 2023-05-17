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
        fontSize=40,
        onclickFunction=None,
        onePress=False,
        image=None,
        imageOffset=(0, 0),
        textOffset=(0, 0),
        fillColors={
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        },
        borderRadius=0,
    ):
        self.x = x
        self.y = y
        self.window = window
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.fontSize = fontSize
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = fillColors
        self.borderRadius = borderRadius
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface = window.subsurface(self.buttonRect)

        self.font = pygame.font.SysFont("Arial", self.fontSize)
        self.fontColor = fontColor
        self.image = pygame.image.load(image) if image is not None else None
        self.imageOffset = imageOffset
        self.textOffset = textOffset

    def process(self):
        mousePos = pygame.mouse.get_pos()
        color = "normal"
        if self.buttonRect.collidepoint(mousePos):
            color = "hover"
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                color = "pressed"
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        pygame.draw.rect(
            self.window,
            self.fillColors[color],
            self.buttonRect,
            border_radius=self.borderRadius,
        )
        text = self.font.render(self.buttonText, True, self.fontColor)
        self.window.blit(
            text,
            text.get_rect(
                center=(
                    self.buttonRect.center[0] + self.textOffset[0],
                    self.buttonRect.center[1] + self.textOffset[1],
                )
            ),
        )
        if self.image is not None:
            self.window.blit(
                self.image,
                (
                    self.buttonRect.center[0] + self.imageOffset[0],
                    self.buttonRect.center[1] + self.imageOffset[1],
                ),
            )
