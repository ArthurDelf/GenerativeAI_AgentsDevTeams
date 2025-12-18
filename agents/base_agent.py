"""
Classe de base pour tous les agents
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_groq import ChatGroq


class BaseAgent(ABC):
    
    
    def __init__(self, name: str, role: str, llm: ChatGroq):
        self.name = name
        self.role = role
        self.llm = llm
        self.thoughts: List[str] = []  
        self.actions: List[Dict[str, Any]] = []  
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        pass
    
    def add_thought(self, thought: str):
        self.thoughts.append(f"[{self.name}] {thought}")
    
    def add_action(self, action: str, result: Any):
        self.actions.append({
            "agent": self.name,
            "action": action,
            "result": result
        })
    
    def reset(self):
        self.thoughts = []
        self.actions = []
    
    def get_trace(self) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "role": self.role,
            "thoughts": self.thoughts.copy(),
            "actions": self.actions.copy()
        }
