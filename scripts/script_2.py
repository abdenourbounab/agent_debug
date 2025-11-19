"""
Script de test 2 - Erreur TypeError
"""

print("Début du script 2...")

def concatener_donnees():
    # Erreur : Tentative de concaténation string + int
    message = "La valeur est : " + 42  # TypeError
    return message

print("Concaténation des données...")
resultat = concatener_donnees()
print(resultat)
