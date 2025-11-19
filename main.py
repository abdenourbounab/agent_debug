"""
Agent de Débogage Python - Point d'entrée principal
Workflow: Exécution → Analyse IA → Patch automatique (EN BOUCLE)
"""
import os
import sys

# Import des modules
from src.executeur import executer_script
from src.ai_debugger import AIDebugger
from src.file_patcher import FilePatcher


def lire_fichier(chemin: str) -> str:
    """Lit le contenu d'un fichier."""
    with open(chemin, 'r', encoding='utf-8') as f:
        return f.read()


def main(script_path: str, auto_apply: bool = True):
    """
    Workflow complet de débogage automatique AVEC BOUCLE.
    Continue à corriger jusqu'à ce qu'il n'y ait plus d'erreurs.
    
    Args:
        script_path: Chemin du script à déboguer
        auto_apply: Si True, applique automatiquement les corrections
    """
    print("=" * 70)
    print("🤖 AGENT DE DÉBOGAGE PYTHON (Mode Boucle Automatique)")
    print("=" * 70)
    print(f"📝 Script: {script_path}")
    print(f"🔄 Mode: Boucle infinie jusqu'à succès")
    print("=" * 70)
    
    venv_python = r"venv\Scripts\python.exe"
    iteration = 0
    total_corrections = 0
    
    # ═══════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE : Continue jusqu'à success
    # ═══════════════════════════════════════════════════════════
    while True:
        iteration += 1
        
        print(f"\n{'🔁' * 35}")
        print(f"🔁 ITÉRATION {iteration}")
        print(f"{'🔁' * 35}")
        
        # ═══════════════════════════════════════════════════════════
        # ÉTAPE 1 : Exécution du script
        # ═══════════════════════════════════════════════════════════
        print("\n📍 ÉTAPE 1/5 : Exécution du script")
        print("-" * 70)
        
        resultat = executer_script(script_path, venv_python)
        
        # Affichage résumé
        status = "✅" if resultat['returncode'] == 0 else "❌"
        print(f"\n{status} Code retour: {resultat['returncode']}")
        
        # ✅ SUCCESS : Sortie de la boucle
        if not resultat['stderr']:
            print("\n" + "=" * 70)
            print("✅ SUCCESS ! Le script fonctionne sans erreur !")
            print(f"📊 Statistiques:")
            print(f"   • Itérations totales: {iteration}")
            print(f"   • Corrections appliquées: {total_corrections}")
            print("=" * 70)
            if resultat['stdout']:
                print(f"\n📤 Sortie du script:\n{resultat['stdout']}")
            return True
    
        # ❌ ERREUR : Continue le cycle de correction
        print(f"\n❌ Erreur détectée:")
        error_preview = resultat['stderr'][:300] if len(resultat['stderr']) > 300 else resultat['stderr']
        print(error_preview)
        
        # ═══════════════════════════════════════════════════════════
        # ÉTAPE 2 : Lecture du code source
        # ═══════════════════════════════════════════════════════════
        print("\n📍 ÉTAPE 2/5 : Lecture du code source")
        print("-" * 70)
        
        code_source = lire_fichier(script_path)
        print(f"✓ {len(code_source)} caractères lus")
    
        # ═══════════════════════════════════════════════════════════
        # ÉTAPE 3 : Analyse par IA
        # ═══════════════════════════════════════════════════════════
        print("\n📍 ÉTAPE 3/5 : Analyse IA des erreurs")
        print("-" * 70)
        
        try:
            debugger = AIDebugger()
            corrections = debugger.analyze_error(
                code=code_source,
                error=resultat['stderr'],
                filename=os.path.basename(script_path)
            )
        except Exception as e:
            print(f"❌ Impossible d'utiliser l'API Groq: {e}")
            print("💡 Utilisez demo_prompt_engineering.py pour mode démo")
            return False
    
        # Affichage des corrections
        if 'corrections' in corrections and corrections['corrections']:
            print(f"✓ {len(corrections['corrections'])} correction(s) proposée(s)\n")
            
            # Afficher les détails des corrections
            print("=" * 70)
            print("📋 DÉTAILS DES CORRECTIONS PROPOSÉES")
            print("=" * 70)
            
            for i, corr in enumerate(corrections['corrections'], 1):
                print(f"\n[Correction {i}]")
                print(f"  📍 Ligne: {corr.get('ligne')}")
                print(f"  🔴 Type d'erreur: {corrections.get('type_erreur', 'N/A')}")
                print(f"  💡 Cause: {corrections.get('cause', 'N/A')}")
                print(f"\n  ❌ Code actuel:")
                print(f"     {corr.get('code_original', 'N/A')}")
                print(f"\n  ✅ Code corrigé:")
                print(f"     {corr.get('code_corrige', 'N/A')}")
                print(f"\n  📝 Explication:")
                print(f"     {corr.get('explication', 'N/A')}")
                print("-" * 70)
            
            if corrections.get('conseil'):
                print(f"\n💬 Conseil: {corrections['conseil']}")
            
            print("\n" + "=" * 70)
        else:
            print("⚠️  Aucune correction proposée - impossible de continuer")
            return False
    
        # ═══════════════════════════════════════════════════════════
        # ÉTAPE 4 : Application du patch
        # ═══════════════════════════════════════════════════════════
        print("\n📍 ÉTAPE 4/5 : Application du patch")
        print("-" * 70)
        
        # Conversion corrections → opérations
        operations = []
        for corr in corrections['corrections']:
            ligne = corr.get('ligne')
            code_corrige = corr.get('code_corrige')
            
            if ligne and code_corrige:
                # Nettoyer le code corrigé (enlever indentation excessive)
                code_corrige = code_corrige.strip()
                
                operations.append({
                    'action': 'replace',
                    'line': ligne,
                    'content': code_corrige
                })
        
        if not operations:
            print("⚠️  Aucune opération valide - impossible de continuer")
            return False
        
        # Résumé des opérations
        print(f"\n📋 {len(operations)} modification(s) à appliquer:")
        for i, op in enumerate(operations, 1):
            print(f"   [{i}] Ligne {op['line']}: Remplacement")
        
        # Demander confirmation
        print(f"\n⚠️  Ces modifications vont être appliquées au fichier:")
        print(f"    📁 {script_path}")
        print(f"    💾 Un backup sera créé automatiquement")
        
        reponse = input("\n❓ Appliquer ces corrections ? (oui/non) : ").strip().lower()
        
        if reponse not in ['oui', 'o', 'yes', 'y']:
            print("❌ Corrections annulées par l'utilisateur - arrêt du processus")
            return False
        
        # Application
        patcher = FilePatcher()
        success = patcher.apply_patch(script_path, operations)
        
        if not success:
            print("❌ Échec du patch - arrêt du processus")
            return False
        
        print("✅ Patch appliqué avec succès")
        total_corrections += 1
        
        # ═══════════════════════════════════════════════════════════
        # FIN DE L'ITÉRATION : La boucle va re-tester automatiquement
        # ═══════════════════════════════════════════════════════════
        print(f"\n🔄 Itération {iteration} terminée - re-test automatique...")
    


if __name__ == "__main__":
    # Script à déboguer
    script = "scripts/script_1.py"
    
    if len(sys.argv) > 1:
        script = sys.argv[1]
    
    print(f"🎯 Script cible: {script}\n")
    
    # Lancer le workflow avec boucle automatique (sans limite)
    success = main(script, auto_apply=True)
    
    if success:
        print("\n🎉 Script corrigé avec succès !")
    else:
        print("\n⚠️  La correction a échoué ou est incomplète")
