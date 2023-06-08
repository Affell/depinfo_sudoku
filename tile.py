import pygame
import algorithme


class Tile:
    def __init__(self, x, y, value, init_value, notes, valid, window, size, bloc_size):
        self.x = x  # Position de la case en abscisse
        self.y = y  # Position de la case en ordonnée
        self.value = value  # Caractère contenu de la case
        self.init_value = init_value  # Contenu inital de la case
        self.notes = notes  # Contenu des notes
        self.valid = valid  # Paramètre vérifiant si la saise du joueur est valide
        self.window = window  # Paramètre spécifiant la surface d'affichage
        self.size = size  # Taille de la case
        self.bloc_size = bloc_size  # Taille des régions de la grille
        self.rect = pygame.Rect(y, x, self.size, self.size)  # Rectangle pygame correspondant à cette case
        self.background_color = "white"  # Couleur du fond
        self.selected = False  # Paramètre vérifiant si la case est saisie ou non

    def draw(self):  # Dessine la case
        surface: pygame.Surface = self.window.subsurface(self.rect)
        surface.fill(self.background_color)
        pygame.draw.rect(self.window, (200, 200, 200), self.rect, 1)

    def display(self):  # Affiche le contenu de la case
        if self.value != "0":
            font = pygame.font.SysFont("Source Sans Pro", 80 - 10 * self.bloc_size)
            color = "red"
            if self.init_value == "0" and self.valid:
                color = "blue"
            elif self.init_value != "0":
                color = "black"
            text = font.render(self.value, True, color)
            self.window.blit(text, text.get_rect(center=self.rect.center))
        elif len(self.notes) > 0:
            font = pygame.font.SysFont("Source Sans Pro", 24 - 3 * self.bloc_size)
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

    def get_pos(self):  # Renvoie la position de la case
        return self.x // self.size, self.y // self.size
