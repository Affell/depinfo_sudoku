from board import Board
from button import Button
import algorithme
import pygame
import pygame_menu
import os
import threading

board: Board = None
difficulties = {
    "Facile": 38,
    "Moyen": 33,
    "Difficile": 30,
    "Expert": 28,
    "Diabolique": 25,
}


def list_grids() -> list[str]:
    return [file[:-7] for file in os.listdir("./grids") if file.endswith(".sudoku")]


def menu_load_grid(name, screen):
    grid, progress, errors = algorithme.lecture_grille(name)
    if algorithme.grille_valide(grid):
        solution = algorithme.resoud_grille(grid)
        if solution is not None:
            global board
            board = Board(name, screen, grid, progress, errors, solution)
        else:
            print(f'Aucune solution n\'a pu être trouvée pour la grille "{name}"')
    else:
        print(f'La grille "{name}" est invalide')


def menu_generate_grid(name, difficulty, screen, menu):
    if len(name.strip()) == 0:
        print("Nom de grille invalide")
        return
    if not os.path.exists(f"./grids/{name}.sudoku"):
        print(f'Génération de la grille "{name}" ({difficulty})...')
        progress_bar = menu.add.progress_bar("Génération", default=0)

        def background_generation():
            grid, solution = algorithme.genere_grille(
                difficulties[difficulty], progress_bar
            )
            global board
            board = Board(name, screen, grid, grid, 0, solution)
            board.save()

        t = threading.Thread(
            target=background_generation, daemon=True, name="Grid generation"
        )
        t.start()

    else:
        print(f'La grille "{name}" existe déjà')


def build_menu(screen) -> pygame_menu.Menu:
    menu = pygame_menu.Menu(
        "Sudoku", 1280, 720, theme=pygame_menu.themes.THEME_DARK, columns=2, rows=2
    )
    load_menu = pygame_menu.Menu(
        "Charger une grille", 1280, 720, theme=pygame_menu.themes.THEME_DARK
    )
    generate_menu = pygame_menu.Menu(
        "Nouvelle grille", 1280, 720, theme=pygame_menu.themes.THEME_DARK
    )

    for grid in list_grids():
        load_menu.add.button(grid, lambda: menu_load_grid(grid, screen))

    name_input = generate_menu.add.text_input("Nom : ")
    difficulty_selector = generate_menu.add.selector(
        "Difficulté : ", [(d,) for d in difficulties.keys()]
    )
    generate_menu.add.button(
        "Valider",
        lambda: menu_generate_grid(
            name_input.get_value(),
            difficulty_selector.get_value()[0][0],
            screen,
            generate_menu,
        ),
    )

    menu.add.button("Charger une grille", load_menu)
    menu.add.button("Nouvelle grille", generate_menu)

    return menu


def game_loop():

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))

    menu: pygame_menu.Menu = build_menu(screen)

    def on_click():
        board.note = not board.note

    note_button: Button = Button(1000, 90, screen, 150, 150, "Note", on_click)

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif board is not None and event.type == pygame.KEYDOWN:
                try:
                    board.enter_digit(int(event.unicode))
                except ValueError as _:
                    pass

        if board is None:
            menu.update(events)
            menu.draw(screen)
        else:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                tile = board.get_tile(*pygame.mouse.get_pos())
                if tile is not None:
                    board.select_tile(tile)

            screen.fill("white")
            board.draw_board()
            note_button.process(board)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
