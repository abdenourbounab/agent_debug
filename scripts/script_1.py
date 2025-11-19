"""
Script de test 1 - Erreurs multiples
Ce script contient plusieurs types d'erreurs pour tester l'agent de débogage
"""

print("Début de l'exécution du script...")

# Erreur 1 : Division par zéro
def division_dangereuse():
    x = 10
    y = 0
    resultat = x / y if y != 0 else 0
    return resultat

# Erreur 2 : Variable non définie
def variable_inexistante():
    print('message_non_defini')

# Erreur 3 : Import inexistant
# import module_qui_nexiste_pas  # Commenter ou supprimer cette ligne si le module n'existe pas

print("Exécution normale...")
resultat = division_dangereuse()
print(f"Résultat : {resultat}")

# Appeler aussi la fonction avec NameError
variable_inexistante()
