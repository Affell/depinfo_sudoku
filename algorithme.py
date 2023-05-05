import numpy as np
import random

grille1 = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7],
]


# Lecture de la grille à partir du fichier


def lecture_grille(name):
    with open(f"./grids/{name}.sudoku", "r") as f:
        lignes = f.readlines()

    init_grid = []
    progress_grid = []
    progress = False
    errors = 0
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne.startswith("PROGRESS:"):
            progress = True
            try:
                errors = int(ligne[9:])
            except Exception:
                continue
        else:
            elements = ligne.split(",")
            ligne_liste = [int(e) for e in elements]
            if progress:
                progress_grid.append(ligne_liste)
            else:
                init_grid.append(ligne_liste)

    return (
        np.array(init_grid),
        np.array(progress_grid) if len(progress_grid) > 0 else np.array(init_grid),
        errors,
    )


# Vérifie de la validité de la grille(on peut ajouter d'autres vérifications)


def grille_valide(grille_jeu):
    compteur = 0
    for i in range(len(grille_jeu)):
        for j in range(len(grille_jeu)):
            case = grille_jeu[i][j]
            if case > 0:
                compteur += 1
    if compteur < 18:
        return False
    for ligne in grille_jeu:
        liste = [e for e in ligne if e != 0]
        if len(set(liste)) != (len(liste)):
            return False

    return True


# Vérification de la validité de la saisie dans la grille (si il n'y a pas de contradiction avec les règles du Sudoku)


def saisie_valide(grille, nb, pos):
    # Vérif ligne
    for i in range(len(grille[0])):
        if grille[pos[0]][i] == nb and pos[1] != i:
            return False

    # Vérif colonne
    for i in range(len(grille)):
        if grille[i][pos[1]] == nb and pos[0] != i:
            return False

    # Vérif carrés
    case_x = pos[1] // 3
    case_y = pos[0] // 3

    for i in range(case_y * 3, case_y * 3 + 3):
        for j in range(case_x * 3, case_x * 3 + 3):
            if grille[i][j] == nb and (i, j) != pos:
                return False

    return True


# Cherche les cases vides dans la grille


def case_vide(grille):
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == 0:
                return (i, j)

    return None


# Algo de backtracking pour résoudre une grille rentrée en paramètre
def resoud_all_grilles(grille):
    return resoud_all_grilles_(np.array(grille))


def resoud_all_grilles_(grille):
    solutions = []
    vide = case_vide(grille)
    if not vide:
        solutions.append(np.array(grille))
        return solutions
    else:
        row, col = vide

    for i in range(1, 10):
        if saisie_valide(grille, i, (row, col)):
            grille[row][col] = i

            for s in resoud_all_grilles_(grille):
                solutions.append(s)

            grille[row][col] = 0

    return solutions


def resoud_grille(grille, randomMode=False):
    return resoud_grille_(np.array(grille), randomMode)[1]


def resoud_grille_(grille, randomMode):
    vide = case_vide(grille)
    if not vide:
        return True, grille
    else:
        row, col = vide
    numbers = [i for i in range(1, 10)]
    if randomMode:
        random.shuffle(numbers)
    for nb in numbers:
        if saisie_valide(grille, nb, (row, col)):
            grille[row][col] = nb

            if resoud_grille_(grille, randomMode)[0]:
                return True, grille

            grille[row][col] = 0

    return False, None


def unicite(solved_grid, grid):
    for _ in range(5):
        if not np.array_equal(resoud_grille(grid, True), solved_grid):
            return False
    return True


def genere_grille(nb, progress_bar=None):
    solution = resoud_grille(np.zeros((9, 9), dtype=np.intp), True)
    grille = np.array(solution)

    cases = [(i, j) for i in range(9) for j in range(9)]
    nb_operations = len(cases) - nb
    for k in range(1, nb_operations + 1):
        (i, j) = None, None
        temp = np.array(grille)
        while (i, j) == (None, None) or not unicite(solution, temp):
            if (i, j) != (None, None):
                temp[i][j] = grille[i][j]
            i, j = random.choice(cases)
            temp[i, j] = 0
        grille[i][j] = 0
        cases.remove((i, j))
        progress_bar.set_value(k / nb_operations * 100)
    return grille, solution
