

from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from .base_agent import BaseAgent

#Product Owner Agent - Analyzes and specifies requirements
class ProductOwnerAgent(BaseAgent):
    def __init__(self, llm: ChatGroq, pdf_context: Optional[str] = None):
        super().__init__(
            name="Product Owner",
            role="Analyste des besoins et créateur de spécifications",
            llm=llm
        )
        self.pdf_context = pdf_context
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour le PO"""
        base_prompt = """Tu es un Product Owner expérimenté dans une équipe de développement.

Ta mission :
1. ANALYSER la demande utilisateur en profondeur
2. IDENTIFIER les fonctionnalités clés
3. CRÉER des User Stories claires et structurées
4. DÉFINIR les critères d'acceptation

Tu dois raisonner étape par étape (Chain of Thought) :
- Étape 1 : Comprendre le besoin métier
- Étape 2 : Identifier les fonctionnalités principales
- Étape 3 : Décomposer en User Stories
- Étape 4 : Définir les critères d'acceptation

Format de sortie attendu :
## Analyse du besoin
[Ton analyse détaillée]

## User Stories
**US1**: [Titre]
- En tant que [utilisateur]
- Je veux [action]
- Afin de [bénéfice]
- Critères d'acceptation :
  - [ ] Critère 1
  - [ ] Critère 2

**US2**: ...

## Contraintes techniques identifiées
- [Liste des contraintes]

Sois PRÉCIS et STRUCTURÉ."""

        if self.pdf_context:
            base_prompt += f"\n\n## Documentation technique disponible :\n{self.pdf_context}"
        
        return base_prompt
    
    def analyze_request(self, user_request: str) -> Dict[str, any]:
        self.thoughts.append(" Début de l'analyse de la demande utilisateur...")
        
        # Construire le prompt
        messages = [
            SystemMessage(content=self._get_system_prompt()),
            HumanMessage(content=f"Demande utilisateur : {user_request}")
        ]
        
        # Appel au LLM
        self.thoughts.append(" Raisonnement en cours (CoT)...")
        response = self.llm.invoke(messages)
        analysis = self._parse_analysis(response.content)
        
        self.thoughts.append(" Analyse termine et User Stories crees")
        
        return {
            "raw_response": response.content,
            "analysis": analysis,
            "thoughts": self.thoughts.copy()
        }
    
    def _parse_analysis(self, response: str) -> Dict[str, any]:
        user_stories = []
        import re
        us_matches = re.findall(r'\*\*US\d+\*\*:', response)
        
        return {
            "full_text": response,
            "user_stories_count": len(us_matches),
            "has_acceptance_criteria": "Critères d'acceptation" in response,
            "has_constraints": "Contraintes techniques" in response
        }
    
    def ask_clarification(self, question: str) -> str:
        """Pose une question de clarification à l'utilisateur"""
        self.thoughts.append(f"❓ Question de clarification : {question}")
        return question


