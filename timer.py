import pygame


class Timer:
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
        start_time = None ,
        elapsed_time = 0,
        minutes = 0,
        seconds = 0,
    ):
        self.x = x
        self.y = y
        self.window = window
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.buttonText = buttonText
        self.fontSize = fontSize
        self.start_time = start_time if start_time is not None else pygame.time.get_ticks()
        self.elapsed_time = elapsed_time
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.SysFont("Arial", self.fontSize)
        self.minutes = minutes
        self.seconds = seconds

    def process(self):
        self.elapsed_time = pygame.time.get_ticks() - self.start_time
        self.minutes = self.elapsed_time // 60000
        self.seconds = (self.elapsed_time // 1000) % 60
        time_text = f"Time: {self.minutes:02d}:{self.seconds:02d}"
        self.buttonText = time_text

        text = self.font.render(self.buttonText, True, self.fontColor)
        
        pygame.draw.rect(
            self.window,
            (255,255,255),
            self.buttonRect,
        )
        self.window.blit(
            text,
            text.get_rect(
                center=(
                    self.buttonRect.center[0],
                    self.buttonRect.center[1],
                )
            ),
        )
