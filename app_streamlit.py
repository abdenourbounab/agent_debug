"""
Interface Streamlit pour l'Agent de Débogage Python
Permet de spécifier le fichier Python et le venv à utiliser
"""
import streamlit as st
import os
import sys

# Import des modules
from src.executeur import executer_script
from src.ai_debugger import AIDebugger
from src.file_patcher import FilePatcher


# ═══════════════════════════════════════════════════════════
# INITIALISATION SESSION STATE
# ═══════════════════════════════════════════════════════════
if 'iteration' not in st.session_state:
    st.session_state.iteration = 0
if 'total_corrections' not in st.session_state:
    st.session_state.total_corrections = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'en_cours' not in st.session_state:
    st.session_state.en_cours = False
if 'attente_confirmation' not in st.session_state:
    st.session_state.attente_confirmation = False
if 'operations_en_attente' not in st.session_state:
    st.session_state.operations_en_attente = None
if 'script_path' not in st.session_state:
    st.session_state.script_path = "scripts/script_1.py"
if 'venv_python' not in st.session_state:
    st.session_state.venv_python = r"venv\Scripts\python.exe"
if 'backup_cree' not in st.session_state:
    st.session_state.backup_cree = False


def lire_fichier(chemin: str) -> str:
    """Lit le contenu d'un fichier."""
    with open(chemin, 'r', encoding='utf-8') as f:
        return f.read()


def demarrer_debogage():
    """Démarre le processus de débogage."""
    st.session_state.en_cours = True
    st.session_state.iteration = 0
    st.session_state.total_corrections = 0
    st.session_state.backup_cree = False
    st.session_state.logs = []
    st.session_state.logs.append("=" * 70)
    st.session_state.logs.append("🤖 AGENT DE DÉBOGAGE PYTHON")
    st.session_state.logs.append("=" * 70)
    
    # Créer un backup unique au début
    try:
        patcher = FilePatcher()
        backup_path = patcher.create_backup(st.session_state.script_path)
        st.session_state.logs.append(f"💾 Backup créé: {backup_path}")
        st.session_state.backup_cree = True
    except Exception as e:
        st.session_state.logs.append(f"⚠️ Impossible de créer le backup: {e}")
    st.session_state.logs.append(f"📝 Script: {st.session_state.script_path}")
    st.session_state.logs.append(f"🐍 Python: {st.session_state.venv_python}")
    st.session_state.logs.append("=" * 70)


def continuer_iteration():
    """Continue une nouvelle itération après confirmation."""
    st.session_state.attente_confirmation = False
    st.session_state.operations_en_attente = None


def annuler_debogage():
    """Annule le débogage en cours."""
    st.session_state.logs.append("\n❌ Débogage annulé par l'utilisateur")
    st.session_state.en_cours = False
    st.session_state.attente_confirmation = False


def executer_iteration():
    """Exécute une itération de débogage."""
    script_path = st.session_state.script_path
    venv_python = st.session_state.venv_python
    
    st.session_state.iteration += 1
    
    # Exécution silencieuse
    resultat = executer_script(script_path, venv_python)
    
    # SUCCESS
    if not resultat['stderr']:
        st.session_state.logs.append("\n" + "=" * 70)
        st.session_state.logs.append("✅ SUCCESS ! Le script fonctionne sans erreur !")
        st.session_state.logs.append(f"📊 Corrections appliquées: {st.session_state.total_corrections}")
        st.session_state.logs.append("=" * 70)
        st.session_state.en_cours = False
        return
    
    # Analyse IA silencieuse
    code_source = lire_fichier(script_path)
    
    try:
        debugger = AIDebugger()
        corrections = debugger.analyze_error(
            code=code_source,
            error=resultat['stderr'],
            filename=os.path.basename(script_path)
        )
    except Exception as e:
        st.session_state.logs.append(f"\n❌ Erreur API: {e}")
        st.session_state.en_cours = False
        return
    
    # Affichage correction (format simplifié)
    if 'corrections' in corrections and corrections['corrections']:
        num_correction = st.session_state.total_corrections + 1
        st.session_state.logs.append(f"\nCorrection {num_correction} :")
        
        for corr in corrections['corrections']:
            st.session_state.logs.append(f"  📍 Ligne: {corr.get('ligne')}")
            st.session_state.logs.append(f"  🔴 Type: {corrections.get('type_erreur', 'N/A')}")
            st.session_state.logs.append(f"  ❌ Code actuel: {corr.get('code_original', 'N/A')}")
            st.session_state.logs.append(f"  ✅ Code corrigé: {corr.get('code_corrige', 'N/A')}")
    else:
        st.session_state.logs.append("\n⚠️  Aucune correction proposée")
        st.session_state.en_cours = False
        return
    
    # Préparation des opérations
    operations = []
    for corr in corrections['corrections']:
        ligne = corr.get('ligne')
        code_corrige = corr.get('code_corrige')
        
        if ligne and code_corrige:
            operations.append({
                'action': 'replace',
                'line': ligne,
                'content': code_corrige.strip()
            })
    
    if not operations:
        st.session_state.logs.append("  ⚠️ Aucune opération valide")
        st.session_state.en_cours = False
        return
    
    # Mettre en attente de confirmation
    st.session_state.attente_confirmation = True
    st.session_state.operations_en_attente = operations


def appliquer_patch():
    """Applique le patch après confirmation."""
    operations = st.session_state.operations_en_attente
    script_path = st.session_state.script_path
    
    patcher = FilePatcher()
    # Ne pas créer de backup (déjà créé au début)
    success = patcher.apply_patch(script_path, operations, create_backup=False)
    
    if not success:
        st.session_state.logs.append("  ❌ Échec de l'application")
        st.session_state.en_cours = False
        st.session_state.attente_confirmation = False
        return
    
    st.session_state.logs.append("  ✅ Appliqué")
    st.session_state.total_corrections += 1
    
    # Réinitialiser et continuer
    st.session_state.attente_confirmation = False
    st.session_state.operations_en_attente = None


# ═══════════════════════════════════════════════════════════
# INTERFACE STREAMLIT
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Agent de Débogage Python",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agent de Débogage Python")
st.markdown("**Correction automatique d'erreurs avec boucle jusqu'à succès**")

st.divider()

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")
    
    # Champs de saisie (désactivés pendant l'exécution)
    script_input = st.text_input(
        "📝 Chemin du script Python",
        value=st.session_state.script_path,
        disabled=st.session_state.en_cours,
        help="Chemin relatif ou absolu vers le fichier .py à déboguer"
    )
    
    venv_input = st.text_input(
        "🐍 Exécutable Python (venv)",
        value=st.session_state.venv_python,
        disabled=st.session_state.en_cours,
        help="Chemin vers l'exécutable Python du virtual environment"
    )
    
    # Mise à jour des valeurs
    if not st.session_state.en_cours:
        st.session_state.script_path = script_input
        st.session_state.venv_python = venv_input
    
    st.divider()
    
    # Vérification des chemins
    script_exists = os.path.exists(st.session_state.script_path)
    venv_exists = os.path.exists(st.session_state.venv_python)
    
    if script_exists:
        st.success(f"✅ Script trouvé")
    else:
        st.error(f"❌ Script introuvable")
    
    if venv_exists:
        st.success(f"✅ Python trouvé")
    else:
        st.error(f"❌ Python introuvable")
    
    st.divider()
    
    # Bouton de démarrage
    if not st.session_state.en_cours:
        if st.button("🚀 Démarrer le Débogage", type="primary", disabled=(not script_exists or not venv_exists)):
            demarrer_debogage()
            st.rerun()

with col2:
    st.subheader("📊 Logs d'exécution")
    
    # Affichage des logs
    if st.session_state.logs:
        st.text_area(
            "Logs",
            value="\n".join(st.session_state.logs),
            height=500,
            label_visibility="collapsed"
        )
    else:
        st.info("👈 Configurez les paramètres et cliquez sur 'Démarrer le Débogage'")
    
    # Gestion du workflow
    if st.session_state.en_cours:
        if st.session_state.attente_confirmation:
            # Afficher les boutons de confirmation
            st.warning("⚠️ Confirmation requise pour appliquer les corrections")
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                if st.button("✅ Oui, appliquer", type="primary", key="apply_btn"):
                    appliquer_patch()
                    st.rerun()
            
            with col_no:
                if st.button("❌ Non, annuler", key="cancel_btn"):
                    annuler_debogage()
                    st.rerun()
        else:
            # Continuer automatiquement l'itération
            executer_iteration()
            st.rerun()
