"""Agent de débogage IA - Analyse d'erreurs Python avec Groq"""
import json
import re
from groq import Groq
import config


class AIDebugger:
    """Agent IA pour analyser erreurs Python et proposer corrections."""
    
    def __init__(self):
        """Initialise l'agent avec Groq AI."""
        try:
            self.client = Groq(api_key=config.GROQ_API_KEY)
            self.model = "llama-3.3-70b-versatile"
            print("✓ Agent de débogage IA activé (Groq)")
        except Exception as e:
            raise Exception(f"Erreur d'initialisation Groq: {e}")
    
    def analyze_error(self, code: str, error: str, filename: str = "script.py") -> dict:
        """Analyse une erreur et propose corrections.
        
        Args:
            code: Code source avec erreur
            error: Message d'erreur complet
            filename: Nom du fichier
        
        Returns:
            dict: Corrections au format JSON
        """
        print(f"\n🔍 Analyse de l'erreur dans '{filename}'...")
        
        try:
            messages = self._build_prompt(code, error, filename)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=1500,
                top_p=0.95
            )
            
            result_text = response.choices[0].message.content.strip()
            corrections = self._parse_response(result_text)
            
            print("✓ Analyse terminée\n")
            return corrections
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return {
                "error": str(e),
                "corrections": [],
                "explication": "Impossible d'analyser l'erreur"
            }
    
    def _build_prompt(self, code: str, error: str, filename: str) -> list:
        """Construit les messages pour l'API Groq."""
        
        system_message = {
            "role": "system",
            "content": """Tu es un EXPERT en débogage Python.

**RÈGLES:**
1. Réponds UNIQUEMENT en JSON valide
2. Fournis des corrections PRÉCISES avec numéros de ligne
3. Propose UNIQUEMENT les corrections nécessaires
4. Explique POURQUOI l'erreur se produit

**FORMAT JSON:**
{
  "type_erreur": "nom de l'exception",
  "ligne_erreur": numéro,
  "cause": "explication",
  "corrections": [
    {
      "ligne": numéro,
      "code_original": "code actuel",
      "code_corrige": "code corrigé (peut être multi-lignes)",
      "explication": "pourquoi cette correction"
    }
  ],
  "conseil": "conseil général"
}

**IMPORTANT pour code_corrige:**
- Donne UNIQUEMENT la ligne corrigée, pas un bloc entier
- Garde la même indentation que la ligne originale
- Pour ZeroDivisionError: remplace "x / y" par "x / y if y != 0 else 0"
- Sois MINIMAL, remplace juste ce qui cause l'erreur"""
        }
        
        user_message = {
            "role": "user",
            "content": f"""Analyse cette erreur Python.

**FICHIER:** {filename}

**CODE:**
```python
{code}
```

**ERREUR:**
```
{error}
```

Réponds en JSON uniquement."""
        }
        
        return [system_message, user_message]
    
    def _parse_response(self, response_text: str) -> dict:
        """Parse la réponse JSON de l'IA."""
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "error": "Réponse JSON invalide",
                "raw_response": response_text[:500],
                "corrections": []
            }
