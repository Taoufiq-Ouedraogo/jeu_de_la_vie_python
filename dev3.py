
############### BIBLIOTHEQUES ###############

from random import *            # pour le remplissage aléatoire des cases
from numpy import *             # pour la création de la matrice
from tkinter import *           # pour l'interface graphique
from time import *              # pour la mise en veille du fonctionnement


############### FONCTIONS ###############


# ----------------------------------------------
# --------------- Initialisation ---------------
# ----------------------------------------------

def initialiser():
    mat = [ [randrange(0, 2) for i in range(taille)] for j in range(taille)]
    return mat



# ------------------------------------------------------------
# --------------- Nombre de voisins d'une case ---------------
# ------------------------------------------------------------

def nb_voisin_vivant(mat, i, j):
    n = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if mat[(i+k)%taille][(j+l)%taille]:
                n+=1
    if mat[i][j]:
         n-=1  # on retire la case en question si elle est vivante
    return n




# ---------------------------------------------------------------
# --------------- Pourcentage de vie de la grille ---------------
# ---------------------------------------------------------------

def pourcentage_vie(mat):
    vivants=0
    total=taille**2     # car matrice carrée
    for i in range(taille):
        for j in range(taille):
            if mat[i][j]==1:
                vivants+=1
    return int(vivants/total*100)       # on veut un pourcentage entier d'après l'énoncé


# ---------------------------------------------------------
# --------------- Survie ou mort d'une case ---------------
# ---------------------------------------------------------

def survie(mat, l, c):
    k=nb_voisin_vivant(mat, l, c)
    if k==2 and damier[l][c]!=0:
        mat[l][c]=1
    elif k==3:
         mat[l][c]=1
    else:                   # la cellule meurt dans tous les autres cas
        mat[l][c]=0
    return mat[l][c]



# -----------------------------------------
# --------------- Affichage ---------------
# -----------------------------------------

def afficher_matrice(mat):      # affichage de la matrice
    for i in range(taille):
        for j in range(taille):
            print(mat[i][j], end='\t')
        print("\n")


def f(mat, mat_suiv):         # affichahe avec tkinter, chaque case est un rectangle
    global damier
    mat_suiv=next_gen(mat, mat_suiv)
    x, y = 0, 0

    scale_vitesse.pack(side=BOTTOM, padx=5, pady=5)
    scale_vie.pack(side=BOTTOM, padx=5, pady=5)
    scale_taille.pack(side=BOTTOM, padx=5, pady=5)

    scale_vie.set(pourcentage_vie(damier))      # on fixe la valeur par défaut du pourcentage sur le scale
    scale_vitesse.set(100-delay)        # on fixe la valeur par défaut de la vitesse sur le scale

    vitesse=scale_vitesse.get()     # pour récupérer la valeur de la vitesse du scale
    vie=scale_vie.get()         # pour récupérer la valeur du pourcentage du scale
    #print(vie, vitesse, delay)          # pour afficher directement sur la console
    for i in range(taille):
        x=0
        for j in range(taille):
            if mat[i][j]!=0:
                # on crée un rectangle pour chaque cellule à la position (x,y) de la toile
                r=toile.create_rectangle(x, y, x+block_size, y+block_size, fill="blue")
            else:
                r=toile.create_rectangle(x, y, x+block_size, y+block_size, fill="ivory")
            x+=block_size   # on incrémente x pour passer à la case suivante
        y+=block_size       # on incrémente y pour passer à la ligne suivante
    fenetre.after(delay, f, mat, mat_suiv)     # Exécute la fonction après delay temps d'attente



# ----------------------------------------------------------------
# --------------- Passage à la génération suivante ---------------
# ----------------------------------------------------------------

def next_gen(mat, mat_suiv):
    for i in range(taille):
        for j in range(taille):
            mat_suiv[i][j] = survie(mat, i, j)
    return mat_suiv



# -------------------------------------------------
# --------------- Boutons et Scales ---------------
# -------------------------------------------------

def init():     # initialiser le damier pas à pas
    global damier
    damier = [[0 for j in range(taille)] for i in range(taille)]
    damier=initialiser()
    f(damier, damier_suiv)

def lancer():
    "démarrage de l'animation"
    global go
    if go==0:
        go=1
    print(go)       # confirmer le comportement du bouton
    f(damier, damier_suiv)

def arreter():
    "arrêt de l'animation"
    global go
    go=0
    print(go)       # confirmer le comportement du bouton
    if go ==0:
        sleep(10.0)         # un temps d'attente de 10s
    # fenetre.wait_variable(go)
def accelerer(event):       # on augmente la vitesse en réduisant l'attente de 1 ms
    global delay
    if delay-1>0:
        delay-=1
    else:
        delay=1

def decelerer(event):       # on diminue la vitesse en augmentant l'attente de 1 ms
    global delay
    if delay+1<100:
        delay+=1
    else:
        delay=100


############### EXECUTION ###############


delay=10            # temps d'attente entre 2 générations successives
go = 1              # pour savoir si on doit stopper ou continuer le jeu (ref aux boutons lancer et arreter)
taille= int(input(" Entrer la taille du damier : "))
block_size = 600/taille # en pixels
damier = [[0 for j in range(taille)] for i in range(taille)]
damier_suiv = [[0 for j in range(taille)] for i in range(taille)]

damier=initialiser()



############### INTERFACE GRAPHIQUE ###############


# --------------- initialisation de la fenêtre de travail ---------------
fenetre = Tk()
fenetre['bg']="darkgrey"
fenetre.title("JEU DE LA VIE")


# --------------- canvas ---------------
toile = Canvas(fenetre, width=600, height=600, bg='ivory')

toile.focus_set()
toile.pack(side=LEFT)


# --------------- boutons ---------------
bouton_lancer = Button(fenetre, text="Lancer", bg="grey", width=15, fg="blue", command=lancer)
bouton_arreter = Button(fenetre, text="Arrêter", bg="grey", width=15, fg="blue", command=arreter)
bouton_initialiser = Button(fenetre, text="Initialiser", bg="grey", width=15, fg="blue", command=init)
bouton_quitter = Button(fenetre, text="Quitter", bg="grey", width=15, fg="blue", command=fenetre.destroy)

bouton_lancer.pack(side=TOP,  padx=5)
bouton_arreter.pack(side=TOP, padx=5)
bouton_initialiser.pack(side=TOP, padx=5)
bouton_quitter.pack(side=BOTTOM, padx=5)


# --------------- scales ---------------
scale_vitesse = Scale(fenetre, orient="horizontal",label="Vitesse", bg="grey", fg="blue", highlightbackground="darkgrey")

scale_vie = Scale(fenetre, orient="horizontal", label="% de Vie", bg="grey", fg="blue", highlightbackground="darkgrey")

scale_taille = Scale(fenetre, orient="horizontal", label="Taille grille", bg="grey", fg="blue", highlightbackground="darkgrey")

scale_taille.set(taille)

f(damier, damier_suiv)
toile.bind("<a>", accelerer)        # exécution de l'évènement
toile.bind("<d>", decelerer)        # exécution de l'évènement

print(" appuyer la touche <a> pour accélérer")
print(" appuyer la touche <d> pour décélérer")



fenetre.mainloop()