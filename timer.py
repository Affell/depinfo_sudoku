import pygame


class Timer:
    def __init__(
        self,
        x, # Position de la case en abscisse
        y, # Position de la case en ordonnée
        window, # Paramètre spécifiant la surface d'affichage
        width, # Largeur du timer
        height, # Hauteur du timer
        fontColor, # Couleur de la police d'écriture
        buttonText="Button", # Texte affiché sur le timer
        fontSize=40, # Taille de la police d'écriture
        start_time=None , # Temps auquel le timer est démarré
        elapsed_time=0, # Temps écoulé depuis le lancement du programme
        minutes=0,
        seconds=0,
        stop=False, # Vérifie la marche ou non du timer
    ):
        self.x = x
        self.y = y
        self.window = window
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.buttonText = buttonText
        self.fontSize = fontSize
        self.start_time = (start_time if start_time is not None else pygame.time.get_ticks()) - elapsed_time
        self.last_update = start_time 
        self.elapsed_time = elapsed_time
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)  # Rectangle pygame correspondant au timer
        self.font = pygame.font.SysFont("Arial", self.fontSize) # Police d'éciture
        self.minutes = minutes
        self.seconds = seconds
        self.stop = stop

    def process(self): # Fonction qui permet de créer le timer
        if not self.stop:
            self.elapsed_time += pygame.time.get_ticks() - self.last_update
        self.minutes = self.elapsed_time // 60000
        self.seconds = (self.elapsed_time // 1000) % 60
        time_text = f"Time: {self.minutes:02d}:{self.seconds:02d}"
        self.buttonText = time_text

        text = self.font.render(self.buttonText, True, self.fontColor)

        pygame.draw.rect(
            self.window,
            (255, 255, 255),
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
        self.last_update = pygame.time.get_ticks()
