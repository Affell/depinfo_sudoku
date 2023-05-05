import numpy as np
import random

# Lecture de la grille à partir du fichier
def lecture_grille(name):
    with open(f"./grids/{name}.sudoku", "r") as f:
        lignes = f.readlines()

    init_grid = []
    progress_grid = []
    notes = []
    progress = False
    note = False
    noteMode = False
    errors = 0
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne.startswith("PROGRESS:"):
            noteMode = False
            progress = True
            try:
                errors = int(ligne[9:])
            except Exception:
                continue
        elif ligne.startswith("NOTES:"):
            progress = False
            note = True
            try:
                noteMode = ligne[6:] == "True"
            except Exception:
                continue
        else:
            elements = ligne.split(",")
            if note:
                ligne_liste = [[n for n in e.split("|") if n != ""] for e in elements]
                notes.append(ligne_liste)
            else:
                ligne_liste = [e for e in elements]
                if progress:
                    progress_grid.append(ligne_liste)
                else:
                    init_grid.append(ligne_liste)

    return (
        np.array(init_grid),
        np.array(progress_grid) if len(progress_grid) > 0 else np.array(init_grid),
        notes,
        noteMode,
        errors,
    )


def get_allowed_characters(taille, zeros=True):
    return (["0"] if zeros else []) + (
        [str(i) for i in range(1, 10)] + [chr(i) for i in range(65, 91)]
    )[:taille]


def get_character_index(char):
    return ord(char) - 48 if 49 <= ord(char) <= 57 else ord(char) - 55


# Vérifie de la validité de la grille(on peut ajouter d'autres vérifications)


def grille_valide(grille_jeu):
    for ligne in grille_jeu:
        liste = [e for e in ligne if e != "0"]
        if len(set(liste)) != (len(liste)):
            return False

    return True


# Vérification de la validité de la saisie dans la grille (si il n'y a pas de contradiction avec les règles du Sudoku)


def saisie_valide(grille, char, pos):
    n = len(grille[0])
    m = int((n**0.5))
    # Vérif ligne et colonne
    for i in range(len(grille[0])):
        if grille[pos[0]][i] == char and pos[1] != i:
            return False
        elif grille[i][pos[1]] == char and pos[0] != i:
            return False

    # Vérif carrés
    case_x = pos[1] // m
    case_y = pos[0] // m

    for i in range(case_y * m, case_y * m + m):
        for j in range(case_x * m, case_x * m + m):
            if grille[i][j] == char and (i, j) != pos:
                return False

    return True


# Cherche les cases vides dans la grille


def case_vide(grille):
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == "0":
                return (i, j)

    return None


# Algo de backtracking pour résoudre une grille rentrée en paramètre
def resoud_all_grilles(grille):
    return resoud_all_grilles_(
        np.array(grille), get_allowed_characters(len(grille), False)
    )


def resoud_all_grilles_(grille, chars):
    solutions = []
    vide = case_vide(grille)
    if not vide:
        solutions.append(np.array(grille))
        return solutions
    else:
        row, col = vide

    for char in chars:
        if saisie_valide(grille, char, (row, col)):
            grille[row][col] = char

            for s in resoud_all_grilles_(grille, chars):
                solutions.append(s)

            grille[row][col] = "0"

    return solutions


def resoud_grille(grille, randomMode=False):
    return resoud_grille_(
        np.array(grille), get_allowed_characters(len(grille), False), randomMode
    )[1]


def resoud_grille_(grille, chars, randomMode):
    vide = case_vide(grille)
    if not vide:
        return True, grille
    else:
        row, col = vide
    if randomMode:
        random.shuffle(chars)
    for char in chars:
        if saisie_valide(grille, char, (row, col)):
            grille[row][col] = char

            if resoud_grille_(grille, chars, randomMode)[0]:
                return True, grille

            grille[row][col] = "0"

    return False, None


def unicite(solved_grid, grid):
    for _ in range(5):
        if not np.array_equal(resoud_grille(grid, True), solved_grid):
            return False
    return True


def genere_grille(nb, taille, progress_bar=None):
    solution = resoud_grille(np.full((taille, taille), "0", dtype=str), True)
    grille = np.array(solution)

    cases = [(i, j) for i in range(taille) for j in range(taille)]
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
        if progress_bar is not None:
            progress_bar.set_value(k / nb_operations * 100)
    return grille, solution
