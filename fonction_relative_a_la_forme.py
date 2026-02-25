# Projet Python : Comme un air de Tetris
# Réalisé par Mathieu Alassoeur et Nathan Germany
# Ce fichier reprend toutes les fonctions relatives à la forme que l'utilisateur choisis. Ainsi elle permet de supprimer
# les lignes de la grille et/ou de dessiner la forme dans la console. Malheureusement il y a certaines fonctions qui ne
# fonctionnent pas mais nous avons laissé la fonction "brouillon" comme celle pour supprimer une ligne.


import fonction_affichage_console as f2
import fonction_relative_aux_blocs as f3


def choisir_forme():
    # Cette fonction comme son nom l'indique demande à l'utilisateur quelle forme il souhaite utiliser
    # cette demande est aussi sécurisée grace à un try except
    z = False
    while not z:
        print("Quelle forme de jeu voulez-vous choisir : ")
        print("Triangle(1)")
        print("Losange(2)")
        print("Cercle(3)")
        h = 0
        while h != 1 and h != 2 and h != 3:
            try:
                h = int(input(""))
            except:
                print("La valeur n'est pas bonne recommencez !")
                choisir_forme()
        z = True
        if h == 1:
            dessiner_forme(1)
        elif h == 2:
            dessiner_forme(2)
        elif h == 3:
            dessiner_forme(3)


def dessiner_forme(h):
    # Cette fonction prend un paramètre un nombre qui correspond à la forme choisis et appelle la fonction dessiner
    # en conséquence avec la forme du fichier et les blocs de la forme utilisée.
    if h == 1:
        f2.dessiner("triangle.txt", "Formes_pour_Triangle.txt", 3, 0)
    elif h == 2:
        f2.dessiner("losange.txt", "Formes_pour_Losange.txt", 3, 0)
    elif h == 3:
        f2.dessiner("cercle.txt", "Formes_pour_Cercle.txt", 3, 0)


def renvoie_forme_en_grid(forme_en_txt, forme):
    # cette fonction prend en paramètre la forme du texte et les blocs correspondants, renvoie la grille correspondante.
    f3.ajoute_les_deux_fichiers_blocs(forme)
    with open(forme_en_txt, "r") as fichier2:
        # Lecture du fichier ouvert
        contenu = fichier2.readlines()
    return contenu


def ligne_effacer(grid, i):
    # Cette fonction n'est pas opérationnelle mais elle permettait de retirer une ligne en cherchant
    # le premier et le dernier 1 d'une ligne.
    print(i)
    premier1 = cherchepremier1(grid, i)
    print(premier1)
    dernier1 = cherchedernier1(grid, i)
    print(dernier1)
    if i >= 1:
        for j in range(1, i + 1):
            for y in range(premier1, dernier1 + 1):
                if grid[i - j][y] != 0:
                    grid[i - j + 1][y] = grid[i - j][y]
                else:
                    grid[i - j + 1][y] = 1
    if i == 0:
        for y in range(premier1, dernier1 + 1):
            grid[i][y] = 1
    return grid


def colonne_effacer(grid, i):
    # Cette fonction n'est pas opérationnelle mais elle permettaient de retirer une colonne lorsqu'elle comportait plus
    # de 1
    for j in range(i, 0, -1):
        grid[j] = grid[j - 1]
        print(j)
        print(grid[j])


def cherchepremier1(grid, i):
    # Cette fonction permet de chercher le premier 1 de la ligne
    print(grid)
    for y in range(len(grid[i])):
        if grid[i][y] == 2:
            return y


def cherchedernier1(grid, i):
    # Cette fonction permet de chercher le dernier 1 de la ligne
    print(grid)
    for y in range(len(grid[i]) - 1, -1, -1):
        if grid[i][y] == 2:
            return y


def retirer_la_colonne(grid, scores):
     # Nous n'avons malheureusement pas eu le temps d'ajouter cette fonction dans le programme car elle fonctionne
     # pas complètement. Mais nous pensons qu'elle devrait réussir à fonctionner en la modifiant un petit peu. Elle
     # permettait de retirer une colonne
    colonne = []
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            colonne.append(grid[j][i])
        grid = supprimer_colonne(grid, colonne, scores, i)
        colonne = []
    return grid


def supprimer_colonne(grid, colonne, score, i):
    # Idem que la fonction ci dessus cette fonction est appelée dans cette dernière.
    if 1 not in colonne:
        for k in range(0, len(grid)):
            if grid[k][i] == 2:
                grid[k][i] = 1
                score += 1
    return grid


def supprimer_ligne(grid, score):
    # Encore une fois cette fonction permettait de supprimer une ligne mais elle ne fonctionne pas encore mais,
    # bientot avec un peu plus de temps.
    for i in range(len(grid)):
        if 1 not in grid[i]:
            for j in range(0, len(grid[i])):
                if grid[i][j] == 2:
                    grid[i][j] = 1
                    score += 1