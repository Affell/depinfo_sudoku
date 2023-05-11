from board import Board
from button import Button
import algorithme
import pygame
import pygame_menu
import os
import threading

board: Board = None
sizes = {"4x4": 4, "9x9": 9, "16x16": 16}
difficulties = {
    "4x4": {
        "Facile": 6,
        "Moyen": 5,
    },
    "9x9": {
        "Facile": 38,
        "Moyen": 33,
        "Difficile": 30,
        "Expert": 28,
        "Diabolique": 25,
    },
    "16x16": {
        "Facile": 160,
        "Moyen": 145,
        "Difficile": 135,
        "Expert": 125,
        "Diabolique": 115,
    },
}


def list_grids() -> list[str]:
    return [file[:-7] for file in os.listdir("./grids") if file.endswith(".sudoku")]


def menu_load_grid(name, screen):
    grid, progress, notes, noteMode, errors = algorithme.lecture_grille(name)
    if algorithme.grille_valide(grid):
        solution = algorithme.resoud_grille(grid, 1)
        if len(solution) == 1:
            global board
            board = Board(
                name, screen, grid, progress, notes, noteMode, errors, solution[0]
            )
        else:
            print(f'Aucune solution n\'a pu être trouvée pour la grille "{name}"')
    else:
        print(f'La grille "{name}" est invalide')


def menu_generate_grid(name, size, difficulty, screen, menu):
    if len(name.strip()) == 0:
        print("Nom de grille invalide")
        return
    if not os.path.exists(f"./grids/{name}.sudoku"):
        print(f'Génération de la grille "{name}" ({difficulty})...')
        progress_bar = menu.add.progress_bar("Génération", default=0)

        def background_generation():
            grid, solution = algorithme.genere_grille(
                difficulties[size][difficulty], sizes[size], progress_bar
            )
            global board
            board = Board(name, screen, grid, grid, [], False, 0, solution)
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
        btn = load_menu.add.button(
            grid, lambda name: menu_load_grid(name, screen), grid
        )

    name_input = generate_menu.add.text_input("Nom : ")
    size_selector = generate_menu.add.selector(
        "Taille : ", [(s,) for s in sizes.keys()]
    )
    difficulty_selector = generate_menu.add.selector(
        "Difficulté : ",
        [(d,) for d in difficulties[size_selector.get_value()[0][0]].keys()],
    )
    size_selector.set_onchange(
        lambda size: difficulty_selector.update_items(
            [(d,) for d in difficulties[size[0][0]].keys()]
        )
    )
    generate_menu.add.button(
        "Valider",
        lambda: menu_generate_grid(
            name_input.get_value(),
            size_selector.get_value()[0][0],
            difficulty_selector.get_value()[0][0],
            screen,
            generate_menu,
        ),
    )

    menu.add.button("Charger une grille", load_menu)
    menu.add.button("Nouvelle grille", generate_menu)

    return menu


def game_loop():

    global board
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))

    menu: pygame_menu.Menu = build_menu(screen)

    note_button: Button = Button(
        1000,
        90,
        screen,
        100,
        100,
        "red",
        buttonText="Note",
        image="./resources/note-button.png",
    )

    def on_click():
        board.noteMode = not board.noteMode

    note_button.onclickFunction = on_click

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                if board is not None:
                    board.save()
                running = False
            elif board is not None and event.type == pygame.KEYDOWN:
                try:
                    board.enter_char(event.unicode.upper())
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
            note_button.fontColor = "green" if board.noteMode else "red"
            note_button.process()

            if board.error_count == 3:
                board.show_error_message()
                

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
