# =============================================================================
# INTERFACE GRAPHIQUE DU SYSTEME DE RECOMMANDATION
# =============================================================================

# =============================================================================
# 1️⃣ IMPORTATION DES BIBLIOTHEQUES
# =============================================================================

import tkinter as tk            # Bibliothèque principale pour créer l'interface graphique
from tkinter import ttk         # ttk permet d'utiliser des widgets Tkinter plus modernes
import pandas as pd             # Bibliothèque utilisée pour manipuler les données (dataset CSV)
from IA.Algorithme import recommander # Importer la fonction IA de recommandation, cette fonction est définie dans le fichier Algorithme.py

 
# =============================================================================
# 2️⃣ CHARGER LES PRODUITS DEPUIS LE DATASET
# =============================================================================

# Lire le fichier CSV contenant les historiques d’achats
# DATA/Achats.csv est le dataset utilisé par l'algorithme de recommandation
data = pd.read_csv("DATA/Achats.csv")

# Extraire la liste des produits uniques présents dans la colonne "product"
# unique() → récupère les valeurs sans répétition
# sorted() → trie les produits par ordre alphabétique
produits = sorted(data["product"].unique())

# =============================================================================
# 3️⃣ FONCTION DE RECOMMANDATION
# Cette fonction sera appelée lorsque l'utilisateur clique sur le bouton
# =============================================================================

def Envoi():

    # récupérer le produit sélectionné dans le menu déroulant
    produit = combo.get()

    # vider la liste des résultats précédente dans la listbox
    # 0 → premier élément
    # tk.END → dernier élément
    listbox.delete(0, tk.END)

    # appeler la fonction IA qui va générer les recommandations
    # cette fonction analyse les achats dans le dataset
    resultats = recommander(produit)

    # vérifier si aucune recommandation n'a été trouvée
    if not resultats:

        # afficher un message dans la liste
        listbox.insert(tk.END, "Aucune recommandation trouvée")

    else:

        # parcourir la liste des produits recommandés
        for item in resultats:

            # ajouter chaque produit dans la listbox
            listbox.insert(tk.END, item)


# =============================================================================
# 4️⃣ CREATION DE LA FENETRE PRINCIPALE
# =============================================================================

# création de la fenêtre principale de l'application
root = tk.Tk()

# définir le titre affiché dans la barre supérieure de la fenêtre
root.title("Système IA de recommandation")

# définir la taille de la fenêtre (largeur x hauteur)
root.geometry("500x350")

# définir la couleur de fond de la fenêtre
root.configure(bg="#f2f2f2")

# =============================================================================
# 5️⃣ TITRE DE L'APPLICATION
# =============================================================================

# création d'un label servant de titre principal
title = tk.Label(

    root,                                   # la fenêtre dans laquelle le label est affiché
    text="Système de recommandation produits", # texte affiché
    font=("Arial", 16, "bold"),              # police : Arial taille 16 en gras
    bg="#f2f2f2"                             # couleur de fond du label
)

# afficher le titre dans la fenêtre
# pady ajoute un espace vertical
title.pack(pady=10)

# =============================================================================
# 6️⃣ MENU DEROULANT POUR SELECTIONNER UN PRODUIT
# =============================================================================

# création d'un frame (conteneur) pour organiser les éléments
frame_input = tk.Frame(root, bg="#f2f2f2")

# afficher le frame dans la fenêtre
frame_input.pack(pady=10)


# création d'un label pour indiquer à l'utilisateur quoi faire
label = tk.Label(

    frame_input,                # le label est placé dans le frame
    text="Choisir un produit :",# texte affiché
    bg="#f2f2f2"                # couleur de fond
)
# placer le label à gauche du menu déroulant
label.pack(side=tk.LEFT, padx=5)

# =============================================================================
# 7️⃣ MENU DEROULANT DES PRODUITS
# =============================================================================

# création du menu déroulant (Combobox)
combo = ttk.Combobox(

    frame_input,      # le menu déroulant est placé dans le frame
    values=produits,  # liste des produits chargés depuis le dataset
    width=20          # largeur du menu
)
# afficher le menu déroulant
combo.pack(side=tk.LEFT)

# définir la valeur par défaut sélectionnée (premier produit)
combo.current(0)

# =============================================================================
# 8️⃣ BOUTON POUR LANCER LA RECOMMANDATION
# =============================================================================

# création du bouton qui déclenche la recommandation
btn = tk.Button(

    root,                        # bouton placé dans la fenêtre principale
    text="Obtenir recommandation", # texte affiché sur le bouton
    command=Envoi    # fonction exécutée lors du clic
)
# afficher le bouton
btn.pack(pady=10)

# =============================================================================
# 9️⃣ AFFICHAGE DES RESULTATS
# =============================================================================

# label indiquant la zone de résultats
label_res = tk.Label(
    root,
    text="Produits recommandés :", # texte affiché
    font=("Arial", 12),            # police utilisée
    bg="#f2f2f2"
)
# afficher le label
label_res.pack()


# création de la listbox (liste) pour afficher les recommandations
listbox = tk.Listbox(
    root,
    width=40,   # largeur de la liste
    height=8    # nombre de lignes visibles
)
# afficher la liste dans la fenêtre
listbox.pack(pady=10)

# =============================================================================
# 🔟 LANCER L'APPLICATION
# =============================================================================

# boucle principale de Tkinter
# elle permet de maintenir la fenêtre ouverte et d'attendre les actions utilisateur
root.mainloop()