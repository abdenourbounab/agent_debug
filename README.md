# 🤖 Agent de Débogage Python

> Système intelligent qui détecte, analyse et corrige automatiquement les erreurs Python avec l'IA Groq

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-green.svg)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Fonctionnel-success.svg)]()

---

## 📋 Table des Matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Fonctionnalités](#-fonctionnalités)
3. [Structure du projet](#-structure-du-projet)
4. [Installation](#-installation)
5. [Utilisation](#-utilisation)
6. [Architecture](#-architecture)

---

## 🎯 Vue d'ensemble

Agent intelligent de débogage automatique qui :
- ✅ **Exécute** des scripts Python et capture les erreurs
- ✅ **Analyse** les erreurs avec l'IA Groq (llama-3.3-70b-versatile)
- ✅ **Corrige** automatiquement le code source
- ✅ **Boucle** jusqu'à ce que le script fonctionne sans erreur
- ✅ **Valide** chaque correction avec confirmation utilisateur
- ✅ **Sauvegarde** automatique unique avant toute modification

### Workflow automatique

```
Script bugué → Exécution → Erreur détectée → Analyse IA → Correction proposée
                ↑                                                    ↓
                └────────────────────── Validation utilisateur ←────┘
                                               ↓
                                         Application → Re-test
```

---

## ✨ Fonctionnalités

### 🔄 Boucle automatique
- Continue à corriger **jusqu'à succès** sans limite d'itérations
- Détecte et corrige les erreurs **une par une** (comportement Python natif)
- Pas besoin de relancer manuellement le script

### 🎨 Interface Streamlit
- **Deux champs configurables** : chemin du script + chemin du venv Python
- **Vérification automatique** de l'existence des fichiers
- **Logs en temps réel** avec affichage minimaliste
- **Confirmation interactive** pour chaque correction

### 💾 Gestion des backups
- **Un seul backup** créé au début du processus
- Pas de backups multiples qui encombrent le dossier
- Format : `script_name.py.backup_YYYYMMDD_HHMMSS`

### 🧹 Logs épurés
Format minimaliste et clair :
```
Correction 1 :
  📍 Ligne: 20
  🔴 Type: ModuleNotFoundError
  ❌ Code actuel: import module_qui_nexiste_pas
  ✅ Code corrigé: # import module_qui_nexiste_pas
  ✅ Appliqué

Correction 2 :
  📍 Ligne: 12
  🔴 Type: ZeroDivisionError
  ❌ Code actuel: resultat = x / y
  ✅ Code corrigé: resultat = x / y if y != 0 else 0
  ✅ Appliqué

======================================================================
✅ SUCCESS ! Le script fonctionne sans erreur !
📊 Corrections appliquées: 2
======================================================================
```

---

## 📁 Structure du projet

```
Agent_debug/
├── 📂 src/                      # Modules principaux
│   ├── executeur.py             # Exécution et capture d'erreurs
│   ├── ai_debugger.py           # Analyse IA avec Groq API
│   ├── file_patcher.py          # Système de patch avec validation
│   └── __init__.py
│
├── 📂 scripts/                  # Scripts de test avec erreurs
│   ├── script_1.py              # Multi-erreurs (3 types)
│   ├── script_2.py              # TypeError
│   ├── script_3.py              # AttributeError
│   └── script_4.py              # KeyError
│
├── 📂 backups/                  # Sauvegardes automatiques
├── 📂 venv/                     # Environnement virtuel Python
│
├── 🎯 main.py                   # CLI - Ligne de commande
├── 🌐 app_streamlit.py          # Interface web Streamlit ⭐
├── ⚙️ config.py                  # Configuration (API keys)
├── 🔒 .env                       # Variables d'environnement
└── 📖 README.md                 # Documentation
```

---

## 🚀 Installation

### 1. Prérequis

- Python 3.11+
- Clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

### 2. Cloner le projet

```powershell
git clone <repo-url>
cd Agent_debug
```

### 3. Créer l'environnement virtuel

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```powershell
pip install groq python-dotenv streamlit
```

### 5. Configurer l'API Groq

Créer un fichier `.env` à la racine :

```env
GROQ_API_KEY=gsk_votre_cle_api_ici
```

---

## 💻 Utilisation

### 🌐 Interface Streamlit (Recommandé)

```powershell
.\venv\Scripts\python.exe -m streamlit run app_streamlit.py
```

L'application s'ouvre automatiquement dans votre navigateur sur **http://localhost:8501**

**Fonctionnalités :**
- 📝 Champ pour le chemin du script Python
- 🐍 Champ pour le chemin du Python (venv)
- ✅ Vérification automatique des fichiers
- 🚀 Bouton "Démarrer le Débogage"
- 📊 Logs en temps réel
- ⚠️ Confirmation avant chaque correction
- 🔄 Boucle automatique jusqu'à succès

### 🖥️ Ligne de commande (CLI)

```powershell
# Script par défaut (scripts/script_1.py)
.\venv\Scripts\python.exe main.py

# Script spécifique
.\venv\Scripts\python.exe main.py scripts/script_2.py
```

---

## 🏗️ Architecture

### Modules principaux

#### 1. `src/executeur.py`
```python
def executer_script(script_path: str, python_exe: str) -> dict:
    """
    Exécute un script Python et capture stdout/stderr/returncode.
    """
```

#### 2. `src/ai_debugger.py`
```python
class AIDebugger:
    def analyze_error(self, code: str, error: str, filename: str) -> dict:
        """
        Analyse l'erreur avec Groq AI et retourne des corrections structurées.
        Modèle : llama-3.3-70b-versatile
        """
```

#### 3. `src/file_patcher.py`
```python
class FilePatcher:
    def apply_patch(self, file_path: str, operations: list, create_backup: bool = True) -> bool:
        """
        Applique les corrections avec validation syntaxique et backup optionnel.
        """
```

### Flux de données

```
┌─────────────┐
│   Script    │
│   Python    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  Executeur  │────▶│  Erreur ?    │
│  (subprocess)│     └──────┬───────┘
└─────────────┘            │ Oui
                           ▼
                   ┌───────────────┐
                   │  AI Debugger  │
                   │  (Groq API)   │
                   └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │ Confirmation  │◀── Utilisateur
                   │  utilisateur  │
                   └───────┬───────┘
                           │ Oui
                           ▼
                   ┌───────────────┐
                   │ File Patcher  │
                   │ (apply_patch) │
                   └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │   Re-test     │
                   └───────┬───────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
           ▼                               ▼
    ┌──────────┐                   ┌──────────┐
    │ Erreur ? │                   │ SUCCESS  │
    │   Oui    │                   │    ✅    │
    └────┬─────┘                   └──────────┘
         │
         └──────────┐
                    │
                    ▼
            (Boucle automatique)
```

---

## 🧪 Scripts de test

| Script | Erreur(s) | Description |
|--------|-----------|-------------|
| `script_1.py` | **ModuleNotFoundError**<br>**ZeroDivisionError**<br>**NameError** | Script multi-erreurs pour tester la boucle automatique |
| `script_2.py` | **TypeError** | Concaténation string + int |
| `script_3.py` | **AttributeError** | Méthode inexistante sur liste |
| `script_4.py` | **KeyError** | Clé manquante dans dictionnaire |

---

## 🔧 Configuration avancée

### Modifier le modèle Groq

Dans `src/ai_debugger.py` :
```python
response = self.client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Changer ici
    messages=messages,
    temperature=0.3
)
```

Modèles disponibles : `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`, `gemma2-9b-it`

---

## 📝 Notes importantes

- 🔄 **Détection séquentielle** : Python s'arrête à la première erreur, donc les erreurs sont corrigées une par une
- 💾 **Un seul backup** : Créé au début du processus, pas à chaque itération
- ✅ **Validation syntaxique** : Chaque correction est validée avec `ast.parse()` avant application
- 🔒 **Sécurité** : Les fichiers originaux sont sauvegardés dans `backups/` avec timestamp

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Reporter des bugs
- 💡 Proposer des fonctionnalités
- 🔧 Soumettre des pull requests

---

## 📄 Licence

MIT License - Libre d'utilisation et de modification

---

## 👨‍💻 Auteur

Développé avec ❤️ par **Abdenour BOUNAB**

---

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**
