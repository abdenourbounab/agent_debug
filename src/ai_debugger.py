"""Agent de débogage IA - Analyse d'erreurs Python avec Groq"""
import json
import re
import os
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
    
    def _load_prompt(self, prompt_file: str) -> str:
        """Charge un prompt depuis un fichier texte."""
        prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        prompt_path = os.path.join(prompts_dir, prompt_file)
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Fichier de prompt introuvable: {prompt_path}")
    
    def _build_prompt(self, code: str, error: str, filename: str) -> list:
        """Construit les messages pour l'API Groq."""
        
        # Charger les prompts depuis les fichiers
        system_content = self._load_prompt('system_prompt.txt')
        user_template = self._load_prompt('user_prompt.txt')
        
        system_message = {
            "role": "system",
            "content": system_content
        }
        
        # Remplacer les variables dans le template utilisateur
        user_content = user_template.format(
            filename=filename,
            code=code,
            error=error
        )
        
        user_message = {
            "role": "user",
            "content": user_content
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
