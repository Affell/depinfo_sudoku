import numpy as np
import random


def lecture_grille(name):  # Lecture de la grille à partir du fichier
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


def get_allowed_characters(taille, zeros=True):  # Fonction vérifiant la validité des caractères dans la grille
    return (["0"] if zeros else []) + (
        [str(i) for i in range(1, 10)] + [chr(i) for i in range(65, 91)]
    )[:taille]


def get_character_index(char):  # Fonction qui renvoie l'indice d'un caractère ??
    return ord(char) - 49 if 49 <= ord(char) <= 57 else ord(char) - 56


def grille_valide(grille_jeu):  # Vérifie de la validité de la grille(on peut ajouter d'autres vérifications)
    for ligne in grille_jeu:
        liste = [e for e in ligne if e != "0"]
        if len(set(liste)) != (len(liste)):
            return False

    return True


def saisie_valide(grille, char, pos):  # Vérification de la validité d'une saisie dans la grille (si il n'y a pas de contradiction avec les règles du Sudoku)

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


def get_possibilities(grille, chars, randomMode):  # Renvoie les possibilités pour chaque case et celle en ayant le moins
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


def get_next_case(grille, possibilities):  # Renvoie les coordonnées de la prochaine case à remplir
    x, y = None, None
    for i in range(len(possibilities)):
        for j in range(len(possibilities[0])):
            if grille[i][j] == "0" and (
                x is None or len(possibilities[x][y]) > len(possibilities[i][j])
            ):
                x, y = i, j
    return x, y


def update_possibilities(possibilities, case, char):  # Met à jour les possibilités de chaque case
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


def resoud_grille(grille, limit=1, randomMode=False):  # Résoud une grille avec un nombre max de solutions à trouver
    return __resoud_grille(
        np.array(grille), get_allowed_characters(len(grille), False), limit, randomMode
    )


def __resoud_grille(grille, chars, limit, randomMode, possibilities=None):  # Backtracking pour résoudre une grille rentrée en paramètre
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


def genere_grille(nb, taille, progress_bar=None):  # Génère une grille aléatoire
    solution = resoud_grille(np.full((taille, taille), "0", dtype=str), 1, True)[0]
    grille = np.array(solution)

    cases = [(i, j) for i in range(taille) for j in range(taille)]
    nb_operations = len(cases) - nb
    g = __genere_grille(grille, taille, 0, nb_operations, cases, progress_bar)
    return g, solution


def __genere_grille(grille, taille, nb, nb_operations, cases=None, progress_bar=None):
    if cases is None:
        cases = [(i, j) for i in range(taille) for j in range(taille)]
    else:
        cases = [tuple(t) for t in cases]
    if nb == nb_operations:
        return grille
    if len(cases) == 0:
        return None
    random.shuffle(cases)

    temp = np.array(grille)
    for (i, j) in cases:
        if progress_bar is not None:
            progress_bar.set_value(nb / nb_operations * 100)
        temp[i][j] = "0"
        cases.remove((i, j))
        if len(resoud_grille(temp, limit=2)) == 1:
            g = __genere_grille(temp, taille, nb + 1, nb_operations, cases, progress_bar)
            if g is not None:
                return g
        temp[i][j] = grille[i][j]
        cases.append((i, j))
    return None
