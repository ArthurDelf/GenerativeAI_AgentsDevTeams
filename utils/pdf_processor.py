"""
Module de traitement des PDFs - Version Désactivée
(Pour éviter les conflits TensorFlow)
"""

from typing import List, Optional
import os
import tempfile


class PDFProcessor:
    """Classe stub pour PDFs (désactivé pour éviter TensorFlow)"""
    
    def __init__(self):
        """Initialise le processeur de PDFs"""
        self.documents = []
        self.chunks = []
        self.temp_dir = tempfile.mkdtemp()
        print("⚠️ Support PDF temporairement désactivé (conflit TensorFlow)")
    
    def load_pdfs(self, uploaded_files) -> int:
        """
        Charge les PDFs uploadés via Streamlit
        
        Args:
            uploaded_files: Liste des fichiers uploadés
            
        Returns:
            0 (désactivé)
        """
        print("⚠️ Chargement PDF désactivé temporairement")
        return 0
    
    def search(self, query: str, k: int = 3) -> List[str]:
        """Recherche désactivée"""
        return []
    
    def get_context_for_agent(self, query: Optional[str] = None, k: int = 5) -> str:
        """
        Retourne un message indiquant que les PDFs sont désactivés
        
        Returns:
            Message informatif
        """
        return "Support PDF temporairement désactivé."
    
    def get_summary(self) -> str:
        """Retourne un résumé des PDFs chargés"""
        return "⚠️ Support PDF temporairement désactivé (conflit avec TensorFlow)"
    
    def cleanup(self):
        """Nettoie les fichiers temporaires"""
        import shutil
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass


# Fonction helper pour Streamlit
def display_pdf_info(processor):
    """Affiche les informations des PDFs dans Streamlit"""
    import streamlit as st
    st.info("ℹ️ Support PDF temporairement désactivé")


