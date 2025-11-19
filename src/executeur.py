"""Exécuteur de scripts Python avec capture stdout/stderr"""
import subprocess
import sys
import os


def executer_script(chemin_script, venv_python=None):
    """Exécute un script Python et capture les sorties.
    
    Args:
        chemin_script: Chemin vers le script à exécuter
        venv_python: Chemin Python du venv (optionnel)
    
    Returns:
        dict: {'stdout': str, 'stderr': str, 'returncode': int}
    """
    python_executable = venv_python if (venv_python and os.path.exists(venv_python)) else sys.executable
    print(f"✓ Python utilisé: {python_executable}")
    
    if not os.path.exists(chemin_script):
        return {'stdout': '', 'stderr': f"Fichier inexistant: {chemin_script}", 'returncode': -1}
    
    print(f"✓ Exécution: {chemin_script}\n" + "=" * 60)
    
    try:
        resultat = subprocess.run(
            [python_executable, chemin_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {'stdout': resultat.stdout, 'stderr': resultat.stderr, 'returncode': resultat.returncode}
    
    except subprocess.TimeoutExpired:
        return {'stdout': '', 'stderr': "Timeout dépassé (10s)", 'returncode': -1}
    except Exception as e:
        return {'stdout': '', 'stderr': f"Erreur: {e}", 'returncode': -1}
