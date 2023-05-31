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
    timer = 0
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
        elif ligne.startswith("TIMER:"):
            timer = int(ligne[6:])
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
        timer
    )


def get_allowed_characters(taille, zeros=True):
    return (["0"] if zeros else []) + (
        [str(i) for i in range(1, 10)] + [chr(i) for i in range(65, 91)]
    )[:taille]


def get_character_index(char):
    return ord(char) - 49 if 49 <= ord(char) <= 57 else ord(char) - 56


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


def get_possibilities(grille, chars, randomMode):
    p = [[[] for _ in range(len(grille[i]))] for i in range(len(grille))]
    x, y = None, None
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == "0":
                if randomMode:
                    random.shuffle(chars)
                for char in chars:
                    if saisie_valide(grille, char, (i, j)):
                        p[i][j].append(char)
                if x is None or len(p[x][y]) > len(p[i][j]):
                    x, y = i, j
    return p, (x, y)


def get_next_case(grille, possibilities):
    x, y = None, None
    for i in range(len(possibilities)):
        for j in range(len(possibilities[0])):
            if grille[i][j] == "0" and (
                x is None or len(possibilities[x][y]) > len(possibilities[i][j])
            ):
                x, y = i, j
    return x, y


def update_possibilities(possibilities, case, char):
    new = [
        [[] for _ in range(len(possibilities[i]))] for i in range(len(possibilities))
    ]
    for i in range(len(possibilities)):
        for j in range(len(possibilities[0])):
            if (i, j) != case:
                new[i][j] = [
                    c
                    for c in possibilities[i][j]
                    if not (
                        (i == case[0] and j != case[1])
                        or (i != case[0] and j == case[1])
                        or (
                            i // len(possibilities) ** 0.5
                            == case[0] // len(possibilities) ** 0.5
                            and j // len(possibilities) ** 0.5
                            == case[1] // len(possibilities) ** 0.5
                        )
                    )
                    or c != char
                ]
    return new


# Algo de backtracking pour résoudre une grille rentrée en paramètre
def resoud_grille(grille, limit=1, randomMode=False):
    return __resoud_grille(
        np.array(grille), get_allowed_characters(len(grille), False), limit, randomMode
    )


def __resoud_grille(grille, chars, limit, randomMode, possibilities=None):
    solutions = []
    if possibilities is None:
        possibilities, nextCase = get_possibilities(grille, chars, randomMode)
    else:
        nextCase = get_next_case(grille, possibilities)
    row, col = nextCase
    if nextCase == (None, None):
        solutions.append(np.array(grille))
        return solutions
    for char in possibilities[row][col]:
        grille[row][col] = char
        p = update_possibilities(possibilities, (row, col), char)

        for s in __resoud_grille(grille, chars, limit, randomMode, p):
            solutions.append(s)
            if len(solutions) == limit:
                return solutions

        grille[row][col] = "0"

    return solutions


def genere_grille(nb, taille, progress_bar=None):
    solution = resoud_grille(np.full((taille, taille), "0", dtype=str), 1, True)[0]
    grille = np.array(solution)

    cases = [(i, j) for i in range(taille) for j in range(taille)]
    random.shuffle(cases)
    nb_operations = len(cases) - nb
    for k in range(1, nb_operations + 1):
        temp = np.array(grille)
        (i, j) = None, None
        while (i, j) == (None, None) or len(resoud_grille(temp, limit=2)) > 1:
            if len(cases) == 0:
                return None, solution
            if (i, j) != (None, None):
                temp[i][j] = grille[i][j]
            i, j = cases.pop()
            temp[i][j] = 0
        grille[i][j] = 0
        if progress_bar is not None:
            progress_bar.set_value(k / nb_operations * 100)
    return grille, solution
