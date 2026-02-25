# Projet Python : Comme un air de Tetris
# Réalisé par Mathieu Alassoeur et Nathan Germany
# Ce fichier permet de demander à l'utilisateur de faire ses premiers choix tel que, est-ce qu'il souhaite lancer la
# partie ou plutôt lire les règles, d'autre part on affiche aussi un pixel art.


import fonction_relative_a_la_forme as f1


def debut_du_jeu():
    # La fonction début du jeu permet d'afficher d'abord un pixel art du jeu Tetris et ensuite de demander que
    # souhaite faire l'utilisiteur grâce à une autre fonction.
    with open("Interface_debut.txt", "r") as pixel:
        pixel_art = pixel.readlines()
        for ligne in pixel_art:
            for cara in ligne:
                if cara == "1":
                    print(" ■", end="")
                if cara == "0":
                    print(" .", end="")
            print("")
    a = "Bienvenue"
    b = "==========================="
    print(b.center(80))
    print(a.center(80))
    print(b.center(80))
    n = lancement_partie()
    if n == 1:
        f1.choisir_forme()
    elif n == 2:
        print("Voici les règles:")
        print("Le Projet jeu Tetris consiste à inserer des blocs que l'ordinateur donnera à placer en essayant "
              "d'empiler le maximum de bloc entre eux pour pouvoir augmenter son score. ")
        print("Dans le jeu l'utilisateur possède trois vies c'est à dire qu'il a le droit de donner deux mauvaises "
              "coordonnées au maximum sinon il perd automatiquement. ")
        print("Il y a une règle en plus qui est que l'utilisateur a le droit de placer un bloc sur un bloc déjà "
              "existant.")
        g = str(input("Après avoir lu ces quelques lignes, voulez-vous jouer ?(oui ou non)"))
        if g == "oui":
            f1.choisir_forme()
        else:
            print("Dommage, bon dimanche")
    else:
        print("Le nombre n'est pas valide choisissez 1 ou 2")


def lancement_partie():
    # Cette fonction permet de demander à l'utilisateur s'il souhaite lancer le jeu ou afficher les règles,
    # de plus il y a une commande sécurisé grâce au try except
    g = False
    n = None
    while not g:
        print("Voulez-vous lancer une partie ?(1)")
        print("Voulez-vous lire les règles ?(2)")
        n = 0
        while not g:
            # utilisation du try pour éviter de crash le programme
            try:
                n = int(input(""))
            except:
                print("La valeur n'est pas bonne recommencez !")
                n = int(input(""))
            if n == 1:
                g = True
            if n == 2:
                g = True
    return n
