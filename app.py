import streamlit as st
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="AI_Dev Team",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .agent-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 AI_Dev Team</h1>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 1.2rem; color: #666;'>"
    "Votre équipe de développeurs IA qui code, teste et livre pour vous"
    "</p>",
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("📋 Configuration")
    
    # API Key
    st.subheader("🔑 API Configuration")
    api_choice = st.selectbox(
        "Choisissez votre LLM",
        ["Groq (Gratuit)", "Ollama (Local)", "OpenAI (Payant)"]
    )
    
    if api_choice == "Groq (Gratuit)":
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Obtenez votre clé gratuite sur https://console.groq.com"
        )
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
            st.success("✅ API Key configurée")
    
    st.divider()
    
    # Upload PDFs
    st.subheader("📤 Documentation Technique")
    uploaded_files = st.file_uploader(
        "Uploadez vos PDFs (specs, API docs, exemples...)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Ces documents seront analysés par l'équipe"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} fichier(s) chargé(s)")
        for file in uploaded_files:
            st.markdown(f"- 📄 `{file.name}`")
    
    st.divider()
    
    
    with st.expander("⚙️ Options Avancées"):
        max_iterations = st.slider(
            "Nombre maximum d'itérations",
            min_value=1,
            max_value=5,
            value=2,
            help="Combien de fois le code peut être revu/corrigé"
        )
        
        show_reasoning = st.checkbox(
            "Afficher le raisonnement détaillé",
            value=True,
            help="Montre les pensées internes de chaque agent"
        )
        
        auto_fix = st.checkbox(
            "Correction automatique",
            value=True,
            help="Le Dev corrige automatiquement les bugs détectés par QA"
        )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Décrivez votre besoin")
    user_request = st.text_area(
        "Que voulez-vous que l'équipe développe ?",
        placeholder="Exemple : Créer un script Python qui récupère les données météo d'une ville via l'API OpenWeatherMap, "
        "gère les erreurs réseau, et sauvegarde les résultats dans un fichier CSV.",
        height=150
    )
    
    # Exemples rapides
    with st.expander("💡 Exemples de requêtes"):
        if st.button("📊 Script d'analyse de données CSV"):
            user_request = "Créer un script qui charge un CSV, calcule des statistiques descriptives, et génère des graphiques avec matplotlib"
        if st.button("🌐 Client API REST"):
            user_request = "Implémenter un client Python pour l'API GitHub qui récupère les repos d'un utilisateur avec gestion d'authentification et pagination"
        if st.button("🤖 Web scraper"):
            user_request = "Créer un scraper qui extrait les titres et liens des articles de Hacker News avec BeautifulSoup"

with col2:
    st.header("👥 L'Équipe")
    st.markdown("""
    **Product Owner** 🎯  
    _Analyse et spécifie_
    
    **Lead Developer** 💻  
    _Code la solution_
    
    **QA Engineer** 🐛  
    _Teste et critique_
    
    **Tech Lead** ✅  
    _Valide et décide_
    """)

# Bouton de lancement
st.divider()

if st.button("🚀 Lancer l'équipe", type="primary", use_container_width=True):
    if not user_request:
        st.error("⚠️ Veuillez décrire votre besoin avant de lancer l'équipe")
    elif api_choice == "Groq (Gratuit)" and not groq_api_key:
        st.error("⚠️ Veuillez configurer votre API Key Groq dans la barre latérale")
    else:
        # Sauvegarder la configuration dans session_state
        st.session_state.user_request = user_request
        st.session_state.uploaded_files = uploaded_files
        st.session_state.max_iterations = max_iterations
        st.session_state.show_reasoning = show_reasoning
        st.session_state.auto_fix = auto_fix
        st.session_state.api_key = groq_api_key
        st.session_state.running = True
        st.rerun()

# Zone d'exécution
if st.session_state.get("running", False):
    st.divider()
    st.header("🔄 Exécution en cours...")
    
    # Importer les modules nécessaires
    from langchain_groq import ChatGroq
    from orchestrator import TeamOrchestrator
    from utils.pdf_processor import PDFProcessor
    import zipfile
    import io
    
    # Initialiser le LLM
    llm = ChatGroq(
        model="moonshotai/kimi-k2-instruct-0905",
        temperature=0.3,
        api_key=st.session_state.api_key
    )
    
    # Traiter les PDFs si présents
    pdf_context = None
    if st.session_state.uploaded_files:
        with st.status("📄 Traitement des PDFs...") as pdf_status:
            processor = PDFProcessor()
            num_docs = processor.load_pdfs(st.session_state.uploaded_files)
            pdf_context = processor.get_context_for_agent()
            pdf_status.update(label=f"✅ {num_docs} pages chargées", state="complete")
    
    # Créer l'orchestrateur
    orchestrator = TeamOrchestrator(llm=llm, pdf_context=pdf_context)
    
    # Exécuter le workflow
    with st.status("L'équipe travaille...", expanded=True) as status:
        # Placeholder pour l'exécution en temps réel
        progress_placeholder = st.empty()
        
        result = orchestrator.run(
            user_request=st.session_state.user_request,
            max_iterations=st.session_state.max_iterations,
            auto_fix=st.session_state.auto_fix
        )
        
        status.update(label="✅ Travail terminé !", state="complete")
    
    # Afficher le résultat
    if result["success"]:
        st.success(f"🎉 Projet validé avec succès en {result['iterations']} itération(s) !")
    else:
        st.warning(f"⚠️ Projet terminé après {result['iterations']} itération(s) - Validation partielle")
    
    # Tabs pour organiser les résultats
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Spécifications",
        "💻 Code",
        "🧪 Tests",
        "✅ Validation",
        "📦 Livraison"
    ])
    
    with tab1:
        st.markdown('<div class="agent-box">', unsafe_allow_html=True)
        st.subheader("🎯 Product Owner - Analyse")
        
        if st.session_state.show_reasoning:
            with st.expander("🧠 Raisonnement (Chain of Thought)"):
                for thought in result["specifications"]["thoughts"]:
                    st.markdown(f"- {thought}")
        
        st.markdown("### User Stories")
        st.markdown(result["specifications"]["user_stories"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="agent-box">', unsafe_allow_html=True)
        st.subheader("💻 Lead Developer - Code")
        
        if st.session_state.show_reasoning:
            with st.expander("🧠 Raisonnement (ReAct)"):
                for thought in result["code"]["thoughts"]:
                    st.markdown(f"- {thought}")
            
            with st.expander("📊 Historique des itérations"):
                st.info(f"Total d'itérations : {result['code']['iterations']}")
        
        st.code(result["code"]["final_code"], language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="agent-box">', unsafe_allow_html=True)
        st.subheader("🐛 QA Engineer - Tests & Critique")
        
        if st.session_state.show_reasoning:
            with st.expander("🧠 Raisonnement (Self-Correction)"):
                for thought in result["tests"]["thoughts"]:
                    st.markdown(f"- {thought}")
        
        # Afficher les bugs
        if result["tests"]["bugs_found"]["critical"]:
            st.markdown("### 🚨 Bugs Critiques")
            for i, bug in enumerate(result["tests"]["bugs_found"]["critical"], 1):
                st.error(f"{i}. {bug}")
        
        if result["tests"]["bugs_found"]["minor"]:
            st.markdown("### ⚠️ Bugs Mineurs")
            for i, bug in enumerate(result["tests"]["bugs_found"]["minor"], 1):
                st.warning(f"{i}. {bug}")
        
        if not result["tests"]["bugs_found"]["critical"] and not result["tests"]["bugs_found"]["minor"]:
            st.success("✅ Aucun bug détecté")
        
        # Score qualité
        if result["tests"]["quality_score"]:
            st.metric("Score Qualité", f"{result['tests']['quality_score']}/10")
        
        # Tests générés
        st.markdown("### Tests Unitaires")
        st.code(result["tests"]["test_code"], language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="agent-box success-box">' if result["success"] else '<div class="agent-box warning-box">', unsafe_allow_html=True)
        st.subheader("✅ Tech Lead - Validation")
        
        if st.session_state.show_reasoning:
            with st.expander("🧠 Raisonnement (Tree of Thoughts)"):
                for thought in result["validation"]["thoughts"]:
                    st.markdown(f"- {thought}")
        
        # Statut
        status_icon = "✅" if result["success"] else "⚠️"
        st.markdown(f"### {status_icon} Statut : {result['validation']['status']}")
        
        # Justification
        if result["validation"]["justification"]:
            st.markdown("### Justification")
            st.markdown(result["validation"]["justification"])
        
        # Actions recommandées
        if result["validation"]["actions"]:
            st.markdown("### Actions Recommandées")
            for i, action in enumerate(result["validation"]["actions"], 1):
                st.markdown(f"{i}. {action}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.subheader("📦 Téléchargement du Projet")
        
        # Créer un ZIP avec tous les fichiers
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Ajouter le code principal
            zip_file.writestr("main.py", result["code"]["final_code"])
            
            # Ajouter les tests
            zip_file.writestr("test_main.py", result["tests"]["test_code"])
            
            # Ajouter le README
            readme_content = f"""# Projet AI Dev Team

## Description
{st.session_state.user_request}

## User Stories
{result["specifications"]["user_stories"]}

## Utilisation
```bash
python main.py
```

## Tests
```bash
pytest test_main.py
```

## Qualité
- Score QA : {result["tests"]["quality_score"]}/10
- Itérations : {result["iterations"]}
- Statut : {result["validation"]["status"]}

---
Généré par AI Dev Team
"""
            zip_file.writestr("README.md", readme_content)
            
            # Ajouter requirements.txt basique
            requirements = "# Dépendances du projet\n# À adapter selon votre code\n"
            zip_file.writestr("requirements.txt", requirements)
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Télécharger le projet complet (.zip)",
            data=zip_buffer,
            file_name=f"ai_dev_team_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            type="primary"
        )
        
        st.info("""
        **Contenu du package :**
        - 📄 `main.py` - Code principal généré
        - 🧪 `test_main.py` - Tests unitaires
        - 📖 `README.md` - Documentation complète
        - 📋 `requirements.txt` - Dépendances
        """)
        
        # Afficher le résumé d'exécution
        with st.expander("📊 Trace d'exécution complète"):
            st.markdown(orchestrator.get_execution_summary())
    
    # Bouton reset
    st.divider()
    if st.button("🔄 Nouvelle demande", type="secondary"):
        # Nettoyer le session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 0.9rem;'>"
    "Projet IA Générative - Agents Intelligents & Raisonnement Avancé"
    "</p>",
    unsafe_allow_html=True
)
