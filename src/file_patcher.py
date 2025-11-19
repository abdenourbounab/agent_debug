"""Système de patch automatique pour modifier fichiers source"""
import os
import shutil
from datetime import datetime
from typing import List, Dict
import ast


class FilePatcher:
    """Système de patch avec backup et validation syntaxique."""
    
    def __init__(self, backup_dir: str = "backups"):
        """Initialise le patcher."""
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, file_path: str) -> str:
        """Crée une sauvegarde avec timestamp."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(self.backup_dir, f"{filename}.backup_{timestamp}")
        
        shutil.copy2(file_path, backup_path)
        print(f"💾 Backup créé: {backup_path}")
        return backup_path
    
    def apply_patch(self, file_path: str, operations: List[Dict], create_backup: bool = True) -> bool:
        """Applique les opérations de patch.
        
        Args:
            file_path: Chemin du fichier
            operations: Liste d'opérations [{"action": "replace", "line": 5, "content": "..."}]
            create_backup: Si True, crée un backup avant modification
        
        Returns:
            bool: True si succès
        """
        try:
            # Backup (optionnel)
            if create_backup:
                backup_path = self.create_backup(file_path)
            
            # Lecture
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Application des opérations (ordre décroissant)
            operations_sorted = sorted(operations, key=lambda x: x.get('line', 0), reverse=True)
            
            for op in operations_sorted:
                action = op.get('action')
                line = op.get('line')
                content = op.get('content', '')
                
                if action == 'replace' and 1 <= line <= len(lines):
                    # Conserver l'indentation de la ligne originale
                    original_line = lines[line-1]
                    original_indent = len(original_line) - len(original_line.lstrip())
                    
                    # Appliquer l'indentation au nouveau contenu
                    content = ' ' * original_indent + content.lstrip()
                    
                    if not content.endswith('\n'):
                        content += '\n'
                    
                    print(f"🔄 Remplacement ligne {line}")
                    lines[line-1] = content
                
                elif action == 'insert':
                    if not content.endswith('\n'):
                        content += '\n'
                    print(f"➕ Insertion ligne {line}")
                    if line == 0:
                        lines = [content] + lines
                    elif line > len(lines):
                        lines.append(content)
                    else:
                        lines = lines[:line-1] + [content] + lines[line-1:]
                
                elif action == 'delete' and 1 <= line <= len(lines):
                    print(f"🗑️  Suppression ligne {line}")
                    lines = lines[:line-1] + lines[line:]
            
            # Écriture
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            # Validation syntaxique
            if not self._validate_syntax(file_path):
                print("❌ Syntaxe invalide - Restauration du backup")
                shutil.copy2(backup_path, file_path)
                return False
            
            print(f"✅ Patch appliqué avec succès ({len(operations)} opération(s))")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du patch: {e}")
            if 'backup_path' in locals():
                shutil.copy2(backup_path, file_path)
            return False
    
    def _validate_syntax(self, file_path: str) -> bool:
        """Valide la syntaxe Python du fichier."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print("✓ Syntaxe Python valide")
            return True
        except SyntaxError as e:
            print(f"✗ Erreur de syntaxe: {e}")
            return False
