

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from .base_agent import BaseAgent

#QA Engineer - Test and critique with Self-Correction
class QAAgent(BaseAgent):
    def __init__(self, llm: ChatGroq):
        super().__init__(
            name="QA Engineer",
            role="Testeur et analyste qualité",
            llm=llm
        )
        self.bugs_found = []
        self.tests_generated = []
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour le QA"""
        return """Tu es un QA Engineer senior expert en Python.

Ta mission : CRITIQUER le code et GÉNÉRER des tests avec Self-Correction.

## Méthodologie Self-Correction
1. **ANALYSE INITIALE** : Examine le code sans préjugé
2. **AUTO-CRITIQUE** : Remets en question ta première analyse
3. **CORRECTION** : Affine ton jugement final

## Format de sortie OBLIGATOIRE :

### 🔍 ANALYSE INITIALE
[Première impression du code]

Points positifs détectés :
- [Point 1]
-[Point 2]

Problèmes potentiels :
- [Problème 1]
- [Problème 2]

###  AUTO-CRITIQUE
"Attendez... est-ce que j'ai bien regardé [aspect] ?"
"Je dois reconsidérer [point]..."

Après réflexion :
- [Correction 1]
- [Correction 2]

###  JUGEMENT FINAL

**Bugs critiques** (blocants) :
1. [Description + ligne concernée + impact]

**Bugs mineurs** (non-blocants) :
1. [Description]

**Améliorations suggérées** :
1. [Suggestion]

**Score de qualité** : X/10

### TESTS UNITAIRES

```python
import pytest

def test_fonction_1():
    \"\"\"Test du cas nominal\"\"\"
    # Arrange
    # Act
    # Assert
    pass

def test_fonction_1_error_handling():
    \"\"\"Test de la gestion d'erreur\"\"\"
    pass
```

## Critères d'évaluation :
-  Gestion d'erreurs complète
- Edge cases couverts
-  Sécurité (injection, validation)
-  Performance (pas de boucles infinies)
-  Maintenabilité (code lisible)
- Respect des standards Python (PEP 8)

Sois RIGOUREUX et CONSTRUCTIF."""
    
    def review_code(self, code: str, user_stories: str) -> Dict[str, any]:
       
        self.add_thought("🔍 Début de la revue de code...")
        
        context = f"""User Stories de référence :
{user_stories}

Code à reviewer :
```python
{code}
```

Effectue une revue complète en utilisant la méthodologie Self-Correction."""

        messages = [
            SystemMessage(content=self._get_system_prompt()),
            HumanMessage(content=context)
        ]
        
        # Appel au LLM
        self.add_thought(" Analyse avec Self-Correction en cours...")
        response = self.llm.invoke(messages)
        
        # Parser la réponse
        parsed = self._parse_review(response.content)
        
        # Sauvegarder les bugs trouvés
        self.bugs_found.extend(parsed["critical_bugs"])
        self.tests_generated.append(parsed["tests"])
        
        self.add_thought(f" Revue terminee : {len(parsed['critical_bugs'])} bugs critiques détectés")
        self.add_action("review_code", f"Bugs: {len(parsed['critical_bugs'])}, Tests générés: {bool(parsed['tests'])}")
        
        return {
            "analysis": parsed["analysis"],
            "critical_bugs": parsed["critical_bugs"],
            "minor_bugs": parsed["minor_bugs"],
            "suggestions": parsed["suggestions"],
            "quality_score": parsed["quality_score"],
            "tests": parsed["tests"],
            "should_fix": len(parsed["critical_bugs"]) > 0,
            "thoughts": self.thoughts.copy(),
            "raw_response": response.content
        }
    
    def _parse_review(self, response: str) -> Dict[str, any]:
        import re
        
        critical_bugs = []
        if "Bugs critiques" in response:
            # Pattern basique : lignes commençant par 1. 2. etc.
            bugs_section = response.split("Bugs critiques")[1].split("**")[0]
            critical_bugs = re.findall(r'\d+\.\s*(.+?)(?=\d+\.|$)', bugs_section, re.DOTALL)
            critical_bugs = [bug.strip() for bug in critical_bugs if bug.strip()]
        
        
        minor_bugs = []
        if "Bugs mineurs" in response:
            bugs_section = response.split("Bugs mineurs")[1].split("**")[0]
            minor_bugs = re.findall(r'\d+\.\s*(.+?)(?=\d+\.|$)', bugs_section, re.DOTALL)
            minor_bugs = [bug.strip() for bug in minor_bugs if bug.strip()]
        
        
        suggestions = []
        if "Améliorations suggérées" in response:
            sugg_section = response.split("Améliorations suggérées")[1].split("**")[0]
            suggestions = re.findall(r'\d+\.\s*(.+?)(?=\d+\.|$)', sugg_section, re.DOTALL)
            suggestions = [sugg.strip() for sugg in suggestions if sugg.strip()]
        
        
        quality_score = None
        score_match = re.search(r'Score.*?(\d+)/10', response)
        if score_match:
            quality_score = int(score_match.group(1))
        
        
        tests = ""
        if "```python" in response:
            # Trouver tous les blocs de code
            code_blocks = re.findall(r'```python\n(.*?)```', response, re.DOTALL)
            if code_blocks:
                tests = code_blocks[-1].strip()  # Prendre le dernier (les tests)
        
        return {
            "analysis": response,  # Full analysis pour affichage
            "critical_bugs": critical_bugs,
            "minor_bugs": minor_bugs,
            "suggestions": suggestions,
            "quality_score": quality_score,
            "tests": tests
        }
    
    def generate_feedback(self, review_result: Dict) -> str:
        
        
        feedback_parts = []
        
        if review_result["critical_bugs"]:
            feedback_parts.append("🚨 BUGS CRITIQUES À CORRIGER :")
            for i, bug in enumerate(review_result["critical_bugs"], 1):
                feedback_parts.append(f"{i}. {bug}")
        
        if review_result["minor_bugs"]:
            feedback_parts.append("\n⚠️ BUGS MINEURS :")
            for i, bug in enumerate(review_result["minor_bugs"], 1):
                feedback_parts.append(f"{i}. {bug}")
        
        if review_result["suggestions"]:
            feedback_parts.append("\n💡 SUGGESTIONS D'AMÉLIORATION :")
            for i, sugg in enumerate(review_result["suggestions"], 1):
                feedback_parts.append(f"{i}. {sugg}")
        
        if review_result["quality_score"]:
            feedback_parts.append(f"\n📊 Score qualité : {review_result['quality_score']}/10")
        
        return "\n".join(feedback_parts)



