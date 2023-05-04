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


def lecture_grille():
    with open("grilles.sudoku", "r") as f:
        lignes = f.readlines()

    grille_jeu = []
    for ligne in lignes:
        ligne = ligne.strip()
        elements = ligne.split(",")
        ligne_liste = [int(e) for e in elements]
        grille_jeu.append(ligne_liste)

    return grille_jeu


# Vérifie de la validité de la grille(on peut ajouter d'autres vérifications)


def grille_valide(grille_jeu):
    valide = False
    compteur = 0
    for i in range(len(grille_jeu)):
        for j in range(len(grille_jeu)):
            case = grille_jeu[i][j]
            if case > 0:
                compteur += 1
        if compteur >= 17:
            valide = True
    for ligne in grille_jeu:
        liste = [e for e in ligne if e != 0]
        if len(set(liste)) != (len(liste)):
            valide = False

    return valide


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


def resoud_grille(grille):
    vide = case_vide(grille)
    if not vide:
        return True
    else:
        row, col = vide

    for i in range(1, 10):
        if saisie_valide(grille, i, (row, col)):
            grille[row][col] = i

            if resoud_grille(grille):
                return True

            grille[row][col] = 0

    return False


grille = lecture_grille()
print(grille1)
print(resoud_grille(grille1))
print(grille1)
