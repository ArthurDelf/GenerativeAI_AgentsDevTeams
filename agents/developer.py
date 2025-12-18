"""
Agent Lead Developer
Responsable de l'écriture du code avec raisonnement ReAct (Reason + Act)
"""

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from .base_agent import BaseAgent

#Lead Developer Agent  Code with ReAct reasoning
class DeveloperAgent(BaseAgent):
    
    
    def __init__(self, llm: ChatGroq):
        super().__init__(
            name="Lead Developer",
            role="Développeur senior Python",
            llm=llm
        )
        self.code_iterations = []
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour le Developer"""
        return """Tu es un Lead Developer Python expérimenté.

Ta mission : ÉCRIRE DU CODE de haute qualité en utilisant le raisonnement ReAct.

## Méthodologie ReAct (Reason + Act)
Tu dois alterner entre PENSÉE et ACTION :

**PENSÉE** : Analyse le problème, planifie l'approche
**ACTION** : Écris le code correspondant
**OBSERVATION** : Évalue ce que tu viens d'écrire
**PENSÉE** : Décide de la prochaine étape

## Format de sortie OBLIGATOIRE :

```reasoning
PENSÉE 1: [Ton analyse du besoin]
ACTION 1: [Ce que tu vas coder]

OBSERVATION 1: [Ce que tu as produit]
PENSÉE 2: [Prochaine étape]
ACTION 2: [Suite du code]
...
```

```python
# Ton code final ici
# Avec commentaires clairs
# Et docstrings

def main():
    \"\"\"Point d'entrée principal\"\"\"
    pass

if __name__ == "__main__":
    main()
```

## Règles de qualité :
- Code PEP 8 compliant
- Docstrings pour fonctions/classes
- Gestion d'erreurs (try/except)
- Type hints quand approprié
- Commentaires pour logique complexe
- Noms de variables explicites

- PAS de code incomplet
- PAS de TODO ou FIXME
- PAS de imports inutiles
- PAS de hardcoded values sensibles

Sois PROFESSIONNEL et RIGOUREUX."""
    
    def generate_code(self, user_stories: str, iteration: int = 1) -> Dict[str, any]:
       
        self.add_thought(f" Début de la génération de code (itération {iteration})")
        
        # Construire le contexte
        context = f"""User Stories à implémenter :
{user_stories}

Génère le code Python complet en suivant la méthodologie ReAct."""

        if iteration > 1:
            # Ajouter l'historique des corrections
            context += f"\n\nCeci est l'itération {iteration}. Voici l'historique :\n"
            for i, prev in enumerate(self.code_iterations, 1):
                context += f"\n--- Itération {i} ---\n"
                if "feedback" in prev:
                    context += f"Feedback QA : {prev['feedback']}\n"
        
        messages = [
            SystemMessage(content=self._get_system_prompt()),
            HumanMessage(content=context)
        ]
        
        # Appel au LLM
        self.add_thought("💭 Raisonnement ReAct en cours...")
        response = self.llm.invoke(messages)
        
        # Parser la réponse
        parsed = self._parse_response(response.content)
        
        # Sauvegarder cette itération
        self.code_iterations.append({
            "iteration": iteration,
            "reasoning": parsed["reasoning"],
            "code": parsed["code"],
            "raw_response": response.content
        })
        
        self.add_thought("✅ Code généré avec succès")
        self.add_action("generate_code", parsed["code"][:100] + "...")
        
        return {
            "code": parsed["code"],
            "reasoning": parsed["reasoning"],
            "iteration": iteration,
            "thoughts": self.thoughts.copy(),
            "raw_response": response.content
        }
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse la réponse pour extraire le raisonnement et le code"""
        
        reasoning = ""
        code = ""
        
        # Extraction du raisonnement
        if "```reasoning" in response:
            start = response.find("```reasoning") + len("```reasoning")
            end = response.find("```", start)
            if end != -1:
                reasoning = response[start:end].strip()
        
        # Extraction du code Python
        if "```python" in response:
            start = response.find("```python") + len("```python")
            end = response.find("```", start)
            if end != -1:
                code = response[start:end].strip()
        else:
            # Fallback : chercher n'importe quel bloc de code
            import re
            code_blocks = re.findall(r'```(\w+)?\n(.*?)```', response, re.DOTALL)
            if code_blocks:
                code = code_blocks[-1][1].strip()  # Prendre le dernier bloc
        
        return {
            "reasoning": reasoning or "Pas de raisonnement structuré détecté",
            "code": code or "# Erreur : Code non généré correctement"
        }
    
    def fix_code(self, feedback: str) -> Dict[str, any]:
        self.add_thought(f" Correction du code basée sur le feedback QA")
        
        # Récupérer la dernière itération
        last_iteration = self.code_iterations[-1]
        last_iteration["feedback"] = feedback
        
        # Générer la correction (nouvelle itération)
        return self.generate_code(
            user_stories=f"Code précédent à corriger :\n{last_iteration['code']}\n\nFeedback QA :\n{feedback}",
            iteration=len(self.code_iterations) + 1
        )


