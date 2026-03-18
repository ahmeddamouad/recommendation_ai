# ============================================================
# SYSTEME DE RECOMMANDATION DE PRODUITS
# Algorithme utilisé : Apriori (association de produits)
# ============================================================


# ============================================================
# 1. IMPORTATION DES BIBLIOTHEQUES
# ============================================================

# pandas : permet de manipuler les données sous forme de tableau
import pandas as pd

# fonctions nécessaires pour l'algorithme de recommandation
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# apriori est une fonction qui vient généralement de la bibliothèque mlxtend
# Elle permet de découvrir :
# des produits fréquemment achetés
# des combinaisons de produits


# ============================================================
# 2. CHARGER LES DONNEES
# ============================================================

# On charge le fichier CSV contenant l'historique des achats
# Chaque ligne représente un achat réalisé par un client

# Exemple du fichier :
# client,product
# Ali,phone
# Ali,headphones
# Sara,phone

data = pd.read_csv("DATA/Achats.csv")

print("=== Données chargées ===")
print(data)


# ============================================================
# 3. CREER LA MATRICE CLIENT - PRODUIT
# ============================================================

# On transforme les données pour obtenir une matrice :
#
# lignes   = clients
# colonnes = produits
# valeur   = 1 si le client a acheté le produit
#
# Exemple :
#
# client   phone   charger   laptop
# Ali        1        0        0
# Sara       1        1        0

# Créer un tableau croisé (table de fréquence) entre les clients et les produits:
matrice_achats = pd.crosstab(data["client"], data["product"])

print("\n=== Matrice client-produit ===")
print(matrice_achats)


# ============================================================
# 4. PREPARER LES DONNEES POUR L'ALGORITHME APRIORI
# ============================================================

# L'algorithme Apriori fonctionne avec True / False, On convertit donc les valeurs 0 et 1 en booléens
matrice_achats = matrice_achats.astype(bool)


# ============================================================
# 5. TROUVER LES PRODUITS fréquemment ACHETES ENSEMBLE 
# ============================================================

# Le code suivant analyse la matrice d'achats (matrice_achats) pour identifier les combinaisons de produits fréquentes.
# min_support = 0.2 signifie : ➡ le produit doit apparaître dans au moins 20 % des achats.

frequent_items = apriori(
    matrice_achats,
    min_support=0.2,
    use_colnames=True
)

print("\n=== Produits fréquemment achetés ===")
print(frequent_items)

# ============================================================
# 6. GENERER LES REGLES DE RECOMMANDATION PAR Apriori algorithm
# ============================================================

# Cette étape affiche un tableau de règles statistiques.
# Chaque ligne dans ce tableau représente une règle de recommandation.
# Les règles permettent de trouver des relations entre les produits, exemple : phone  -> charger
# Cela signifie : les clients qui achètent "phone" achètent souvent aussi "charger"

regles_filtrees = association_rules(
     frequent_items,       # 1️⃣ Les "itemsets fréquents" générés par l'algorithme apriori
     metric="lift",        # 2️⃣ La métrique utilisée pour évaluer la force de chaque règle
     min_threshold=1       # 3️⃣ Le seuil minimum de la métrique pour filtrer les règles
)[["antecedents", "consequents", "lift"]]

# Affiche toutes les règles du DataFrame filtré :
print("\n=== Règles de recommandation ===")
print(regles_filtrees)  

# --1️⃣ frequent_items
# C’est la liste des combinaisons de produits fréquents générée avec apriori().
# Contient des ensembles de produits achetés ensemble plus souvent qu’un certain support minimal.
# Exemple : {phone, charger} avec support = 0.50

# --2️⃣ metric="lift" 
# metric="lift" → vous choisissez de filtrer les règles selon la métrique lift
# lift est une mesure clé dans le projet de système de recommandation de produits;
# elle mesure la probabilité que les deux produits A et B soient achetés ensemble
# Lift mesure ainsi la force de l’association entre les produits.

# lift >= 1 → les produits apparaissent plus souvent ensemble que par hasard → bonne recommandation.
# lift < 1 → les produits apparaissent moins souvent ensemble que par hasard.

# --3️⃣ min_threshold=1
# signifie que Seules les règles dont le lift ≥ 1 seront conservées.
# On élimine donc toutes les règles faibles ou non significatives.

# ------------ antecedents /  consequents 
# antecedents : produit(s) de départ
# consequents : produit(s) recommandés

# Exemple :
# antecedents	consequents
# {phone}	    {charger}

# Cela signifie :
# Si un client achète phone, il achète souvent charger.
# Donc votre système peut recommander charger quand quelqu’un choisit phone.


# ============================================================
# 7. FONCTION DE RECOMMANDATION
# ============================================================

# Cette fonction sera utilisée par l'interface graphique.
# Elle reçoit un produit et retourne les produits recommandés.

def recommander(produit):
    # Etape 1 :
    # Filtrer les règles et garde uniquement les lignes où le produit choisi est dans antecedents.
    # On évite la boucle for et iterrows().
    filtres = regles_filtrees[regles_filtrees["antecedents"].apply(lambda x: produit in x)]
    
    # Etape 2 :
    # Parcourrir tous les ensembles de consequents;    
    # Extraire tous les consequents concernés;
    # set supprime automatiquement les doublons.
    recommandations = set(conseq for row in filtres["consequents"] for conseq in row)
    
    # Transforme l’ensemble en liste pour pouvoir l’afficher dans Tkinter.
    return list(recommandations)