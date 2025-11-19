"""
Script de test 3 - Erreur AttributeError
"""

print("Début du script 3...")

def traiter_liste():
    # Erreur : Appel d'une méthode qui n'existe pas sur une liste
    ma_liste = [1, 2, 3, 4, 5]
    resultat = ma_liste.append_all([6, 7, 8])  # AttributeError
    return resultat

print("Traitement de la liste...")
valeur = traiter_liste()
print(f"Résultat : {valeur}")
