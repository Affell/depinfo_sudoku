from board import Board
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


def list_grids() -> list[str]:  # Renvoie les noms des fichiers présents dans le répertoire
    return [file[:-7] for file in os.listdir("./grids") if file.endswith(".sudoku")]

def menu_load_grid(name, screen):  # Crée le menu de chargement de grille
    grid, progress, notes, noteMode, errors, elapsed_time = algorithme.lecture_grille(name)
    if algorithme.grille_valide(grid):
        solution = algorithme.resoud_grille(grid, 1)
        if len(solution) == 1:
            global board
            board = Board(
                name, screen, grid, progress, notes, noteMode, errors, solution[0], elapsed_time
            )
        else:
            print(f'Aucune solution n\'a pu être trouvée pour la grille "{name}"')
    else:
        print(f'La grille "{name}" est invalide')

def menu_generate_grid(name, size, difficulty, screen, menu):  # Crée le menu de génération de grille
    name = secure_filename(name)
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
            menu.remove_widget(progress_bar)
            global board
            board = Board(name, screen, grid, grid, [], False, 0, solution)
            board.save()

        t = threading.Thread(
            target=background_generation, daemon=True, name="Grid generation"
        )
        t.start()

    else:
        print(f'La grille "{name}" existe déjà')

def menu_solve_grid(name, screen):  # Crée le menu de résolution de grilles
    grid, _, _, _, _, _ = algorithme.lecture_grille(name)
    if algorithme.grille_valide(grid):
        solution = algorithme.resoud_grille(grid, 1)
        if len(solution) == 1:
            global board
            board = Board(
                name, screen, solution[0], solution[0], [], False, 0, solution[0], play=False
            )
        else:
            print(f'Aucune solution n\'a pu être trouvée pour la grille "{name}"')
    else:
        print(f'La grille "{name}" est invalide')

def build_menu(screen) -> tuple[pygame_menu.Menu]:  # Construit les différents menus
    menu = pygame_menu.Menu(
        "Sudoku", 1280, 720, theme=pygame_menu.themes.THEME_DARK, columns=2, rows=3
    )
    load_menu = pygame_menu.Menu(
        "Charger une grille", 1280, 720, theme=pygame_menu.themes.THEME_DARK
    )
    generate_menu = pygame_menu.Menu(
        "Nouvelle grille", 1280, 720, theme=pygame_menu.themes.THEME_DARK
    )
    solve_menu = pygame_menu.Menu(
        "Résoud grille", 1280, 720, theme=pygame_menu.themes.THEME_DARK
    )

    update_menu_grids(screen, load_menu, solve_menu)

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
    menu.add.button("Résoudre grille", solve_menu)

    return menu, load_menu, generate_menu, solve_menu

def update_menu_grids(screen, load_menu, solve_menu):  # Mets à jour les différents menus
    load_menu.clear(False)
    solve_menu.clear(False)
    liste = list_grids()
    if len(liste) == 0:
        load_menu.add.label("Vous n'avez pas de grille enregistrée")
        solve_menu.add.label("Vous n'avez pas de grille enregistrée")
    else:
        for grid in liste:
            load_menu.add.button(
                grid, lambda name: menu_load_grid(name, screen), grid
            )
            solve_menu.add.button(
                grid, lambda name : menu_solve_grid(name, screen), grid
            )

def game_loop():  # Boucle du jeu

    global board
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))

    menu, load_menu, generate_menu, solve_menu = build_menu(screen)

    running = True
    while running:
        if board is not None and not board.active:
            board = None

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                if board is not None:
                    board.save()
                running = False
            elif board is not None and not board.pause and event.type == pygame.KEYDOWN:
                try:
                    board.enter_char(event.unicode.upper())
                except ValueError as _:
                    pass
            if event.type == pygame.KEYDOWN and board is not None:
                board.move_tile(event)

        if board is None:
            if not menu.is_enabled():
                update_menu_grids(screen, load_menu, solve_menu)
                menu.enable()
            menu.update(events)
            menu.draw(screen)
        else:
            if menu.is_enabled():
                menu.disable()
                menu.full_reset()
                board.menus = (menu, load_menu, generate_menu, solve_menu)
            if board.pause_lock and not board.pause and pygame.mouse.get_pressed()[0] == 0:
                board.pause_lock = False
            if not board.pause and not board.pause_lock and pygame.mouse.get_pressed() == (1, 0, 0):
                tile = board.get_tile(*pygame.mouse.get_pos())
                if tile is not None:
                    board.select_tile(tile)

            screen.fill("white")
            board.draw_board()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

def secure_filename(filename: str) -> bool:
    return filename \
        .replace("/", "") \
        .replace("\\", "") \
        .replace(" ", "_") \
        .replace(":", "") \
        .replace("*", "") \
        .replace("?", "") \
        .replace("\"", "") \
        .replace("<", "") \
        .replace(">", "") \
        .replace("|", "") \
        .replace("\0", "")

if __name__ == "__main__":
    os.makedirs("grids", exist_ok=True)
    game_loop()
