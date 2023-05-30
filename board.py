import numpy as np
import pygame
from tile import Tile
import algorithme
from button import Button
from timer import Timer


class Board:
    def __init__(
        self,
        name: str, #Nom de la grille
        window: pygame.Surface, #Paramètre spécifiant la surface d'affichage
        matrix: np.ndarray, #Matrice numpy contenant la grille de sudoku 
        progress: np.ndarray, #Matrice contenant les saisies du joueur
        notes: np.ndarray, #Matrice contenant les notes prises par l'utilisateur
        noteMode, #Paramètre vérifiant si le mode note est activé 
        errors: int, #Compteur d'erreurs
        solution: np.ndarray, #Matrice contenant la solution de la grille
    ):
        self.timer = Timer #Durée de la partie
        self.active = True #??
        self.pause = False #??
        self.name = name #Nom de la grille
        self.init_board = np.array(matrix) #Grille de départ
        self.size = self.init_board.shape[0] #Taille de la grille
        self.bloc_size = int(self.size**0.5) #??
        self.cell_size = int(180 // self.bloc_size) #Taille d'une case
        self.board_size = int(self.size * self.cell_size) #??
        self.current_tile = None #Case actuellement selectionnée
        self.offset = (
            int((1280 - self.board_size) / 2),
            int((720 - self.board_size) / 2),
        ) #Décalage permettant que la grille soit au milieu de l'écran
        self.error_count = errors #Compteur d'erreurs
        self.solution = np.array(solution) #Solution de la grille
        self.screen = window #Surface d'affichage
        self.window = window.subsurface(
            pygame.Rect(*self.offset, self.board_size, self.board_size)
        ) #Surface d'affichage
        self.tiles = [
            [
                Tile(
                    i * self.cell_size,
                    j * self.cell_size,
                    progress[i][j],
                    self.init_board[i][j],
                    notes[i][j] if len(notes) > 0 else [],
                    self.solution[i][j] == progress[i][j],
                    self.window,
                    self.cell_size,
                    self.bloc_size,
                )
                for j in range(self.size)
            ]
            for i in range(self.size)
        ] #Objet Tile qui contient toutes les cases de la grille
        self.noteMode = noteMode #Paramètre vérifiant si le mode note est activé 
        self.error_rect = window.subsurface(pygame.Rect(950, 50, 200, 30)) #??
        self.back_menu = None #Retour au menu
        self.new_game = None #Nouvelle partie

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[i][j].draw()
                self.tiles[i][j].display()
        for i in range(1, int(self.bloc_size) + 1):
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (i * self.cell_size * self.bloc_size, 0),
                (i * self.cell_size * self.bloc_size, self.board_size),
                5,
            )
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (0, i * self.cell_size * self.bloc_size),
                (self.board_size, i * self.cell_size * self.bloc_size),
                5,
            )

        font = pygame.font.SysFont("arial", 20)
        text = font.render(f"Erreurs : {self.error_count}", True, "black")
        self.error_rect.blit(
            text,text.get_rect(center=self.error_rect.get_rect().center)
        )

    def get_tile(self, x, y) -> Tile:
        x -= self.offset[0]
        y -= self.offset[1]
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            return self.tiles[y // self.cell_size][x // self.cell_size]
        return None

    def select_tile(self, tile: Tile):
        pos = tile.get_pos()
        for i in range(self.size):
            for j in range(self.size):
                self.tiles[i][j].selected = False
                if (self.tiles[i][j].value != "0" or (i, j) == pos) and self.tiles[i][
                    j
                ].value == tile.value:
                    self.tiles[i][j].background_color = "green"
                elif (
                    i == pos[0]
                    or j == pos[1]
                    or (i // self.bloc_size, j // self.bloc_size)
                    == (pos[0] // self.bloc_size, pos[1] // self.bloc_size)
                ):
                    self.tiles[i][j].background_color = "gray"
                else:
                    self.tiles[i][j].background_color = "white"
        tile.selected = True
        self.current_tile = tile

    def move_tile(self,event):
        if self.current_tile is None:
            return
        x, y = self.current_tile.get_pos()
        if event.key == pygame.K_UP and x > 0:
            x -= 1
        elif event.key == pygame.K_DOWN and x < self.size - 1:
            x += 1
        elif event.key == pygame.K_LEFT and y > 0:
            y -= 1
        elif event.key == pygame.K_RIGHT and y < self.size - 1:
            y += 1

        self.select_tile(self.tiles[x][y])
        
          
    def enter_char(self, char: str):
        if char not in algorithme.get_allowed_characters(self.size):
            return
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j].selected and self.init_board[i][j] == "0":
                    if self.noteMode:
                        if char != "0":
                            self.tiles[i][j].value = "0"
                            if char in self.tiles[i][j].notes:
                                self.tiles[i][j].notes.remove(char)
                            else:
                                self.tiles[i][j].notes.append(char)
                    else:
                        self.tiles[i][j].notes.clear()
                        self.tiles[i][j].value = char
                        if self.solution[i][j] == char:
                            self.tiles[i][j].valid = True
                        else:
                            self.tiles[i][j].valid = False
                            self.error_count += 1 if char != "0" else 0
                        self.select_tile(self.tiles[i][j])
                    break

    def save(self):
        with open(f"./grids/{self.name}.sudoku", "w") as f:
            f.writelines(
                [",".join([e for e in line]) + "\n" for line in self.init_board]
            )
            f.write(f"PROGRESS:{self.error_count}\n")
            f.writelines(
                [",".join([tile.value for tile in line]) + "\n" for line in self.tiles]
            )
            f.write(f"NOTES:{self.noteMode}\n")
            f.writelines(
                [
                    ",".join(["|".join([note for note in tile.notes]) for tile in line])
                    + "\n"
                    for line in self.tiles
                ]
            )

    def show_error_message(self):
        self.pause = True
        
        gray_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height())
        )
        gray_surface.set_alpha(200)
        gray_surface.fill((0, 0, 0))
        self.screen.blit(gray_surface, (0, 0))

        message_rect = pygame.Rect(
            self.screen.get_width() // 2 - 200,
            self.screen.get_height() // 2 - 100,
            400,
            200,
        )
        pygame.draw.rect(self.screen, (250, 250, 250), message_rect, border_radius=20)

        font = pygame.font.SysFont("arial", 30)
        font2 = pygame.font.SysFont("arial", 20)
        text = font.render("Partie terminée", True, (0, 0, 0))
        text2 = font2.render("Vous avez fait trop d'erreur", True, (186, 186, 186))

        text_rect = text.get_rect(center=message_rect.center)
        text_rect = text_rect.move(0, -35)
        self.screen.blit(text, text_rect)
        text_rect = text.get_rect(center=message_rect.center)
        text_rect = text_rect.move(-10, 5)
        self.screen.blit(text2, text_rect)

        def back_menu_f():
            self.active = False

        self.back_menu: Button = (
            self.back_menu
            if self.back_menu is not None
            else Button(
                message_rect.left + 45,
                message_rect.bottom - 80,
                self.screen,
                155,
                40,
                "white",
                buttonText="Retour à l'accueil",
                fontSize=20,
                onclickFunction=back_menu_f,
                fillColors={
                    "normal": "#0048f9",
                    "hover": "#666666",
                    "pressed": "#0093f9",
                },
                borderRadius=10,
            )
        )

        self.new_game: Button = (
            self.new_game
            if self.new_game is not None
            else Button(
                message_rect.right - 195,
                message_rect.bottom - 80,
                self.screen,
                145,
                40,
                "black",
                buttonText="Nouvelle partie",
                fontSize=20,
                onclickFunction=back_menu_f,
                fillColors={
                    "normal": "#ffffff",
                    "hover": "#dadada",
                    "pressed": "#ffffff",
                },
                borderRadius=10,
            )
        )

    def show_win_message(self):
            self.pause = True
            
            gray_surface = pygame.Surface(
                (self.screen.get_width(), self.screen.get_height())
            )
            gray_surface.set_alpha(200)
            gray_surface.fill((0, 0, 0))
            self.screen.blit(gray_surface, (0, 0))

            message_rect = pygame.Rect(
                self.screen.get_width() // 2 - 200,
                self.screen.get_height() // 2 - 100,
                400,
                200,
            )
            pygame.draw.rect(self.screen, (250, 250, 250), message_rect, border_radius=20)

            font = pygame.font.SysFont("arial", 30)
            font2 = pygame.font.SysFont("arial", 20)
            text = font.render("Partie terminée", True, (0, 0, 0))
            text2 = font2.render("Vous avez gagné", True, (186, 186, 186))

            text_rect = text.get_rect(center=message_rect.center)
            text_rect = text_rect.move(0, -35)
            self.screen.blit(text, text_rect)
            text_rect = text.get_rect(center=message_rect.center)
            text_rect = text_rect.move(20, 5)
            self.screen.blit(text2, text_rect)

            def back_menu_f():
                self.active = False

            self.back_menu: Button = (
                self.back_menu
                if self.back_menu is not None
                else Button(
                    message_rect.left + 45,
                    message_rect.bottom - 80,
                    self.screen,
                    155,
                    40,
                    "white",
                    buttonText="Retour à l'accueil",
                    fontSize=20,
                    onclickFunction=back_menu_f,
                    fillColors={
                        "normal": "#0048f9",
                        "hover": "#666666",
                        "pressed": "#0093f9",
                    },
                    borderRadius=10,
                )
            )

            self.new_game: Button = (
                self.new_game
                if self.new_game is not None
                else Button(
                    message_rect.right - 195,
                    message_rect.bottom - 80,
                    self.screen,
                    145,
                    40,
                    "black",
                    buttonText="Nouvelle partie",
                    fontSize=20,
                    onclickFunction=back_menu_f,
                    fillColors={
                        "normal": "#ffffff",
                        "hover": "#dadada",
                        "pressed": "#ffffff",
                    },
                    borderRadius=10,
                )
            )
