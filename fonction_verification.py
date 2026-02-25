# Projet Python : Comme un air de Tetris
# Réalisé par Mathieu Alassoeur et Nathan Germany
# Ce fichier reprend toutes les fonctions relatives au bon fonctionnement du programme, il y a plusieurs vérifications
# importantes réalisées et les principales sont ici, comme pour vérifier si les coordonnées de l'utilisateurs sont
# valides ou non.


import fonction_relative_a_la_forme as f1
import fonction_affichage_console as f2
import fonction_relative_aux_blocs as f3


def choisir_str(mystr, colonne, n):
    # Cette fonction permet de rajouter le nombre dans la colonne car notre grille est une liste de chaine de
    # caractère donc obligatoirement passer par des slices. Cette fonction renvoie la chaine.
    mystr2 = mystr[:colonne * 2] + n + mystr[(1 + colonne) * 2:]
    return mystr2


def mettre_char_en_grid(Grid, ligne, mystr, colonne, n):
    # Cette fonction permet de modifier la grille pour pouvoir rajouter un bloc a l'intérieur. Elle utilise ainsi
    # la fonction précédente et renvoie la grille modifiée
    mylist = mystr.split(";")
    for id, element in enumerate(mylist):
        if element == '1':
            Grid[ligne] = choisir_str(Grid[ligne], colonne + id, n)
    return Grid


def verifie_si_bonne_coords(x, y, Grid, Bloc, n, score):
    # Cette fonction permet de vérifier si les coordonnées choisis par l'utilisateur sont valides et redemande dans le
    # cas contraire. De plus elle vérifie si le bloc peut être posé ou pas dans la grille, dans le cas où il ne peut pas
    # être posé fait perdre une vie à l'utilisateur
    ab = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"]
    ac = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s"]
    z = x in ac
    t = y in ab
    f10, r, g, w = x, y, None, None
    while not z:
        f10 = str(input("Saisissez une lettre minuscule en abscisse valide"))
        z = f10 in ac
    while not t:
        r = str(input("Saisissez une lettre majuscule en ordonnée valide"))
        t = r in ab
    for i in range(len(ab)):
        if f10 == ac[i]:
            g = i
        if r == ab[i]:
            w = i
    if est_valide(g, w, Grid, Bloc):
        f3.ajouter_bloc(w, g, Bloc, Grid, n, score+5)

    else:
        print("Impossible de placer le bloc à ces coordonnées.")
        print("Vous perdez une vie")
        f2.affichage(Grid, n - 1, score-10)


def est_valide(x, y, Grid, Bloc):
    # Cette fonction permet de vérifier si le bloc est posable dans la grille, renvoie un booléen
    for i in range(x, x + 6):
        for j in range(y, y + 5):
            if (Bloc[(j - y) * 6 + (i - x)] != '0') and (Grid[y][x * 2] != '1'):
                return False
    return True


def verifie_graph(grid, score):
    # Cette fonction n'est pas opérationnelle mais elle permettait de pouvoir changer la grille de str en grille de int
    # et pouvoir faire des changements directement sur la liste de int, ainsi vérifier si dans la grille il y a
    grid = transforme_str_a_int(grid)
    grid = f1.retirer_la_colonne(grid, score)
    score = f2.actualiser_score(score)
    grid = transforme_int_a_str(grid)
    return grid, score


def actualiser_vie(n, z):
    # Cette fonction permet d'afficher le nombre de vie qu'il reste à l'utilisateur.
    if z == 2:
        for i in range(34):
            print(" ", end="")
        print("Vous avez ", end="")
        for i in range(n):
            print("♥ ", end="")
        print("vies", end="")


def transforme_str_a_int(grid):
    # Cette fonction permet de transformer la liste de str en liste de int pour pouvoir changer la valeurs de la liste
    # plus facilement.
    L, J = [], []
    for liste in grid:
        for cara in liste:
            if cara == "0":
                L.append(0)
            if cara == " ":
                L.append(3)
            if cara == "1":
                L.append(1)
            if cara == "2":
                L.append(2)
        J.append(L)
        L = []
    return J


def transforme_int_a_str(grid):
    # Cette fonction permet de transformer la liste de int en liste de str pour pouvoir rechanger la valeurs
    # de la liste.

    L = [[]]
    for i in range(len(grid)):
        L.append([])
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                L[i].append("0")
            if grid[i][j] == 3:
                L[i].append(" ")
            if grid[i][j] == 1:
                L[i].append("1")
            if grid[i][j] == 2:
                L[i].append("2")
    return L