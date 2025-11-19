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
    print('Message non défini')

# Erreur 3 : Import inexistant
# import module_qui_nexiste_pas  # Module supprimé car inexistant

print("Exécution normale...")
resultat = division_dangereuse()
print(f"Résultat : {resultat}")

# Appeler aussi la fonction avec NameError
variable_inexistante()
