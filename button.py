import pygame


class Button:
    def __init__(
        self,
        x, # Position du bouton en abscisse
        y, # Position du bouton en ordonnée 
        window, # Paramètre spécifiant la surface d'affichage
        width, # Largeur du bouton
        height, # Hauteur du boutton
        fontColor, # Couleur de la police d'écriture
        buttonText="Button", # Texte affiché sur le bouton
        fontSize=40, # Taille de la police d'écriture
        onclickFunction=None, # Fonction lancée à l'appui du bouton
        onePress=False, # Paramètre vérifiant si le bouton est pressé
        image=None, # Paramètre permettant d'ajouter un image en fond
        imageOffset=(0, 0), # Décalage de l'image
        textOffset=(0, 0), # Décalage du texte
        fillColors={
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }, # Paramètres spécifiant les différentes couleurs du bouton
        borderRadius=0 # Paramètre permettant d'arrondir les bords du bouton
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
        self.alreadyPressed = False # Paramètre vérifiant si le bouton est déjà pressé
        self.fillColors = fillColors
        self.borderRadius = borderRadius
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)  # Rectangle pygame correspondant à ce bouton
        self.buttonSurface = window.subsurface(self.buttonRect) # Paramètre spécifiant la surface d'affichage
        self.font = pygame.font.SysFont("Arial", self.fontSize) # Paramètre spécifiant la police d'écriture 
        self.fontColor = fontColor
        self.image = pygame.image.load(image) if image is not None else None
        self.imageOffset = imageOffset
        self.textOffset = textOffset

    def process(self): # Fonction qui permet de créer le bouton 
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
