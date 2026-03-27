# Projet Python : Comme un air de Tetris
# Réalisé par Mathieu Alassoeur et Nathan Germany
# Ce fichier reprend toutes les fonctions qui permettent d'afficher des informations dans la console. Il s'agit sans
# doute du fichier le plus important car il permet au bon fonctionnement du jeu.


import fonction_relative_a_la_forme as f1
import fonction_relative_aux_blocs as f3
import fonction_verification as f4


def dessiner(forme_en_txt, forme, n,score):
    # Cette fonction est sans doute la plus importante du projet car elle permet d'afficher toutes les informations
    # dans la console, elle prend en paramètre la forme, les blocs correspondants et le nombre de vies qui reste.
    if n == 0:
        print("Vous avez obtenu un score de ", score," !")
        print("Perdu !")
        return True
    else:
        contenu = f1.renvoie_forme_en_grid(forme_en_txt, forme)
        suite_dessiner(contenu, n, score)


def suite_dessiner(contenu, n, score):
    # Cette fonction correspond à la suite de la fonction dessiner d'où le nom, d'autre part elle prend en paramètre
    # la grille et le nombre de vies restants et elle permet de tout afficher, tel que les blocs, la grille, l'interface
    # ainsi que de demander à l'utilisateur que souhaite-t-il faire.
    p, z = 0, 0
    a = f3.choisit_nombre_aleatoire()
    b = f3.choisit_nombre_aleatoire()
    c = f3.choisit_nombre_aleatoire()
    affichage_abscisses()
    #verifie_graph(grid,score)
    for ligne in contenu:
        affichage_ordonnees_et_graphique(ligne, p)
        z += 1
        p += 1
        afficher_score(z, score)
        f4.actualiser_vie(n, z)
        affichage_piece(z)
        f3.affichage_bloc_ligne_par_ligne(a, z)
        f3.affichage_bloc_ligne_par_ligne(b, z)
        f3.affichage_bloc_ligne_par_ligne(c, z)
        print("")
    print(" ")
    with open("Test.txt", "r") as f2:
        contenu3 = f2.readlines()
    demander_coordonnee(contenu, contenu3[f3.bloc(f3.demander_bloc(), a, b, c)], n, score)
    print("")


def demander_coordonnee(contenu, a, n, score):
    # Cette fonction permet de demander une abscisse et une ordonnée et appelle une autre fonction.
    abscisse = str(input("Saisissez une lettre minuscule en abscisse "))
    ordo = str(input("Saisissez une lettre majuscule en ordonnée "))
    f4.verifie_si_bonne_coords(abscisse, ordo, contenu, a, n, score)


def affichage_ordonnees_et_graphique(ligne, p):
    #Cette fonction prend en paramètre une ligne du grahique et un nombre, elle permet d'afficher les ordonnées grâce à
    # la table ASCII et affiche la ligne du graphique, c'est pourquoi cette fonction est appelée plusieurs fois.
    print(chr(65 + p), end="")
    print("|", end="")
    for caractere in ligne:
        if caractere == "0":
            print("  ", end="")
        if caractere == "1":
            print(" .", end="")
        if caractere == "2":
            print(" ■", end="")


def affichage_abscisses():
    # Cette fonction permet d'afficher les abcisses.
    print("   ", end="")

    for i in range(19):
        print(chr(97 + i), end=" ")
    print("")
    print(" | ", end="")
    for i in range(21):
        print("--", end="")
    print("")


def affichage_piece(z):
    # Cette fonction permet juste d'afficher Voici la pièce en fonction de la ligne utilisée.
    if z == 4:
        for i in range(31):
            print(" ", end="")
        print("=============================", end="")
    if z == 5:
        for i in range(30):
            print(" ", end="")
        print("       Voici les pièces:   ", end="")
    if z == 6:
        for i in range(31):
            print(" ", end="")
        print("=============================", end="")


def affichage(contenu, n, score):
    # Cette fonction à l'instar de la fonction dessiner permet d'afficher le graphique et de vérifier si l'utilisateur
    # a perdu.
    if n == 0:
        print("Vous avez obtenu un score de",score," !")
        print("Perdu !")
        return True
    else:
        suite_dessiner(contenu, n, score)


def afficher_score(z,g):
    # Cette fonction n'est pas opérationnelle mais elle permettait d'afficher le score, mais le score est actualisé
    # lorsqu'on retire une ligne ainsi le score serait toujoues de 0 pour le moment.
    if z == 1:
        for i in range(34):
            print(" ", end="")
        print("Score : ", g, end="")


def actualiser_score(score):
    # Cette fonction tout comme la précédente n'est pas opérationnelle mais permet d'actualiser le score.
    return score + 100