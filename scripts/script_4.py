"""
Script de test 4 - Erreur KeyError
"""

print("Début du script 4...")

def acceder_dictionnaire():
    # Erreur : Accès à une clé inexistante dans un dictionnaire
    utilisateur = {"nom": "Alice", "age": 30}
    email = utilisateur["email"]  # KeyError
    return email

print("Récupération de l'email...")
resultat = acceder_dictionnaire()
print(f"Email : {resultat}")
