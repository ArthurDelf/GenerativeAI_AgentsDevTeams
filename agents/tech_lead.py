"""
Agent Tech Lead
Responsable de la validation finale avec Tree of Thoughts (ToT)
"""

from typing import List, Dict, Optional, Tuple
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from .base_agent import BaseAgent


class TechLeadAgent(BaseAgent):
    """Agent Tech Lead - Valide avec Tree of Thoughts"""
    
    def __init__(self, llm: ChatGroq):
        super().__init__(
            name="Tech Lead",
            role="Architecte et validateur final",
            llm=llm
        )
        self.decisions = []
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour le Tech Lead"""
        return """Tu es un Tech Lead senior avec 15 ans d'expérience.

Ta mission : VALIDER le code et DÉCIDER des actions avec Tree of Thoughts (ToT).

## Méthodologie Tree of Thoughts
Tu dois explorer PLUSIEURS options avant de décider :

1. **GÉNÉRATION D'OPTIONS** : Liste 3 choix possibles
2. **ÉVALUATION** : Analyse avantages/inconvénients de chaque option
3. **ÉLIMINATION** : Écarte les options non viables
4. **DÉCISION FINALE** : Choisis la meilleure option avec justification

## Format de sortie OBLIGATOIRE :

### 🌳 ARBRE DE DÉCISION

**Contexte** : [Résumé de la situation]

**Options explorées** :

#### Option A : [Nom de l'option]
✅ Avantages :
- [Avantage 1]
- [Avantage 2]

❌ Inconvénients :
- [Inconvénient 1]

📊 Évaluation : [Score/10] - [Commentaire]

#### Option B : [Nom de l'option]
✅ Avantages :
- [Avantage 1]

❌ Inconvénients :
- [Inconvénient 1]
- [Inconvénient 2]

📊 Évaluation : [Score/10] - [Commentaire]

#### Option C : [Nom de l'option]
[Même structure]

### 🎯 DÉCISION FINALE

**Option retenue** : [A/B/C]

**Justification** :
[Explication détaillée du choix]

**Actions requises** :
1. [Action 1]
2. [Action 2]

**Statut** : ✅ VALIDÉ | 🔄 À CORRIGER | ❌ REJETÉ

---

## Critères de décision :
- Qualité du code (lisibilité, maintenabilité)
- Sécurité et robustesse
- Performance
- Conformité aux spécifications
- Couverture de tests
- Respect des best practices

Sois STRATÉGIQUE et DÉCISIF."""
    
    def final_review(
        self,
        code: str,
        tests: str,
        user_stories: str,
        qa_report: Dict,
        iteration: int = 1
    ) -> Dict[str, any]:
        """
        Revue finale et décision avec Tree of Thoughts
        
        Args:
            code: Le code à valider
            tests: Les tests unitaires
            user_stories: Les spécifications
            qa_report: Le rapport du QA
            iteration: Numéro de l'itération
            
        Returns:
            Dict avec la décision et les actions
        """
        self.add_thought(f"🌳 Début de la revue finale (itération {iteration})")
        
        # Construire le contexte complet
        context = f"""REVUE FINALE - Itération {iteration}

=== USER STORIES ===
{user_stories}

=== CODE DÉVELOPPÉ ===
```python
{code}
```

=== TESTS UNITAIRES ===
```python
{tests}
```

=== RAPPORT QA ===
Bugs critiques : {len(qa_report.get('critical_bugs', []))}
Bugs mineurs : {len(qa_report.get('minor_bugs', []))}
Score qualité : {qa_report.get('quality_score', 'N/A')}/10

Détails :
{qa_report.get('analysis', 'Pas de rapport détaillé')}

---

En tant que Tech Lead, utilise Tree of Thoughts pour décider :
- Option A : VALIDER le code en l'état
- Option B : DEMANDER des corrections mineures
- Option C : REJETER et demander refonte complète

Évalue chaque option et décide."""

        messages = [
            SystemMessage(content=self._get_system_prompt()),
            HumanMessage(content=context)
        ]
        
        # Appel au LLM
        self.add_thought("💭 Évaluation avec Tree of Thoughts en cours...")
        response = self.llm.invoke(messages)
        
        # Parser la décision
        decision = self._parse_decision(response.content)
        
        # Sauvegarder la décision
        self.decisions.append({
            "iteration": iteration,
            "decision": decision,
            "timestamp": self._get_timestamp()
        })
        
        self.add_thought(f"✅ Décision prise : {decision['status']}")
        self.add_action("final_review", decision['status'])
        
        return {
            "decision": decision,
            "thoughts": self.thoughts.copy(),
            "raw_response": response.content,
            "iteration": iteration
        }
    
    def _parse_decision(self, response: str) -> Dict[str, any]:
        """Parse la réponse pour extraire la décision"""
        
        import re
        
        # Détecter le statut
        status = "UNKNOWN"
        if "✅ VALIDÉ" in response or "VALIDER" in response:
            status = "VALIDATED"
        elif "🔄 À CORRIGER" in response or "CORRIGER" in response:
            status = "NEEDS_CORRECTION"
        elif "❌ REJETÉ" in response or "REJETER" in response:
            status = "REJECTED"
        
        # Extraire l'option retenue
        chosen_option = None
        option_match = re.search(r'Option retenue.*?:\s*([ABC])', response)
        if option_match:
            chosen_option = option_match.group(1)
        
        # Extraire la justification
        justification = ""
        if "Justification" in response:
            parts = response.split("Justification")[1].split("**")[0]
            justification = parts.strip()
        
        # Extraire les actions requises
        actions = []
        if "Actions requises" in response:
            actions_section = response.split("Actions requises")[1].split("**")[0]
            actions = re.findall(r'\d+\.\s*(.+?)(?=\d+\.|$)', actions_section, re.DOTALL)
            actions = [action.strip() for action in actions if action.strip()]
        
        return {
            "status": status,
            "chosen_option": chosen_option,
            "justification": justification,
            "actions": actions,
            "full_analysis": response
        }
    
    def should_iterate(self, decision: Dict) -> Tuple[bool, str]:
        """
        Détermine si une nouvelle itération est nécessaire
        
        Returns:
            (should_continue, reason)
        """
        if decision["status"] == "VALIDATED":
            return False, "Code validé"
        elif decision["status"] == "NEEDS_CORRECTION":
            return True, "Corrections mineures nécessaires"
        elif decision["status"] == "REJECTED":
            return True, "Refonte complète requise"
        else:
            return False, "Statut inconnu"
    
    def _get_timestamp(self) -> str:
        """Retourne le timestamp actuel"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_final_report(self) -> str:
        """Génère un rapport final de toutes les décisions prises"""
        
        if not self.decisions:
            return "Aucune décision enregistrée"
        
        report = ["# RAPPORT TECH LEAD", ""]
        
        for dec in self.decisions:
            report.append(f"## Itération {dec['iteration']} - {dec['timestamp']}")
            report.append(f"**Statut** : {dec['decision']['status']}")
            
            if dec['decision']['chosen_option']:
                report.append(f"**Option choisie** : {dec['decision']['chosen_option']}")
            
            if dec['decision']['justification']:
                report.append(f"\n**Justification** :\n{dec['decision']['justification']}")
            
            if dec['decision']['actions']:
                report.append("\n**Actions** :")
                for i, action in enumerate(dec['decision']['actions'], 1):
                    report.append(f"{i}. {action}")
            
            report.append("\n---\n")
        
        return "\n".join(report)

