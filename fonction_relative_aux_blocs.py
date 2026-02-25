# Projet Python : Comme un air de Tetris
# Réalisé par Mathieu Alassoeur et Nathan Germany
# Ce fichier reprend toutes les fonctions relatives aux blocs, il s'agit des fonctions qui permettent d'afficher les
#blocs, de les choisir aléatoirement, d'ajouter les deux fichiers blocs entre eux...


import fonction_affichage_console as f2
import fonction_verification as f4


def demander_bloc():
    # Cette fonction permet de demander quel bloc souhaite choisir l'utilisateur et de renvoyer la réponse.
    g = 0
    while (g!=1) and (g!=2) and (g!=3):
        try:
            g = int(input("Vous voulez choisir quel bloc ? (1,2 ou 3)"))
        except:
            print("Recommencez la valeur que vous avez choisis n'est pas bonne")
            g = int(input("Vous voulez choisir quel bloc ? (1,2 ou 3)"))
    return g


def bloc(z, a, b, c):
    # Cette fonction permet de prendre en paramètre un nombre qui est le résultat de demander_bloc ainsi que les 3 blocs
    # et de retourner le bloc choisis en conséquence.
    if z == 1:
        return a
    if z == 2:
        return b
    if z == 3:
        return c


def choisit_nombre_aleatoire():
    # Cette fonction permet de choisir un nombre aleatoire entre 0 et le nombre de blocs qu'il y a au maximum, et
    # renvoie ce nombre.
    import random
    with open("Test.txt", "r") as f2:
        contenu3 = f2.readlines()
        return random.randint(0, len(contenu3) - 1)


def ajoute_les_deux_fichiers_blocs(forme_en_txt):
    # Cette fonction prend en paramètre la liste des blocs de la forme choisis au début, et elle permet d'écrire dans
    # nouveau fichier la liste de tous les blocs utilisables pendant le jeu.
    with open(forme_en_txt, "r") as f9, open("commun.txt", "r") as f3:
        contenu = f9.readlines()
        contenu2 = f3.readlines()
    with open("Test.txt", "w") as f2:
        for i in contenu:
            f2.write(i)
        f2.write("")
        for j in contenu2:
            f2.write(j)


def affichage_bloc(h, g):
    # Cette fonction prend en paramètre le bloc et un nombre, elle permet d'afficher la ligne correspondante au nombre
    # g.
    for i in range(((g - 1) * 6), g * 6 - 1):
        if h[i] == "1":
            print(" ■", end="")
        if h[i] == "0":
            print(" .", end="")


def affichage_bloc_ligne_par_ligne(u, z):
    # Cette fonction utilise directement la fonction précédente car elle affiche ainsi chaque ligne du bloc dans la
    # console, une par une.
    with open("Test.txt", "r") as fichier2:
        # Lecture du fichier ouvert
        contenu3 = fichier2.readlines()
    if z == 7:
        for i in range(15):
            print(" ", end="")
        affichage_bloc(contenu3[u], 5)
    if z == 8:
        for i in range(15):
            print(" ", end="")
        affichage_bloc(contenu3[u], 4)
    if z == 9:
        for i in range(15):
            print(" ", end="")
        affichage_bloc(contenu3[u], 3)
    if z == 10:
        for i in range(15):
            print(" ", end="")
        affichage_bloc(contenu3[u], 2)
    if z == 11:
        for i in range(15):
            print(" ", end="")
        affichage_bloc(contenu3[u], 1)


def ajouter_bloc(ligne, colonne, bloc, grid, n, score):
    # Cette fonction permet d'ajouter le bloc dans la grille grâce aux deux autres fonctions qui vérifiaient la colonne
    # et la ligne.
    j = ""
    for cara in bloc:
        if cara != ";":
            j = j + cara + ";"
        if cara == ";":
            grid = f4.mettre_char_en_grid(grid, ligne, j, colonne, " 2")
            ligne -= 1
            j = ""
    grid = f4.mettre_char_en_grid(grid, ligne, j, colonne, " 2")
    f2.affichage(grid, n, score)