# 🚀 AI Dev Team - Équipe de Développement IA

> Projet IA Générative - Agents Intelligents, Raisonnement Avancé & Streamlit

Une application Streamlit qui simule une équipe complète de développeurs IA capables de raisonner, coder, tester et valider du code Python de manière autonome.

---

## 📋 Description du Projet

**AI Dev Team** est une application multi-agents qui transforme une description textuelle en un projet Python complet, testé et validé. L'équipe est composée de 4 agents spécialisés, chacun utilisant une technique de raisonnement avancée :

### 🤖 L'Équipe

| Agent | Rôle | Technique de Raisonnement |
|-------|------|---------------------------|
| **🎯 Product Owner** | Analyse les besoins et crée les spécifications | **Chain of Thought (CoT)** |
| **💻 Lead Developer** | Génère le code Python | **ReAct (Reason + Act)** |
| **🐛 QA Engineer** | Critique le code et génère les tests | **Self-Correction** |
| **✅ Tech Lead** | Valide et décide des actions | **Tree of Thoughts (ToT)** |

---

## ✨ Fonctionnalités

**Multi-agents collaboratifs** : 4 agents spécialisés qui communiquent entre eux  
**Support PDF** : Uploadez des spécifications techniques, documentation d'API, exemples  
**Raisonnement explicite** : Visualisez comment chaque agent pense et décide  
**Itérations automatiques** : Le code est amélioré jusqu'à validation  
**Tests unitaires** : Génération automatique de tests pytest  
**Export complet** : Téléchargez un projet ZIP prêt à l'emploi  
**API gratuite** : Fonctionne avec Groq (LLaMA 3.1 70B)  

---

## 🏗️ Architecture

```
User Request + PDFs
        ↓
┌───────────────────┐
│  Product Owner    │ → User Stories (CoT)
│  📋 Analyse       │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  Lead Developer   │ → Code Python (ReAct)
│  💻 Code          │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  QA Engineer      │ → Tests + Critique (Self-Correction)
│  🐛 Tests         │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│  Tech Lead        │ → Validation (ToT)
│  ✅ Validation    │   ↓
└───────────────────┘   ├─ VALIDÉ ✓
                        ├─ À CORRIGER → Retour au Dev
                        └─ REJETÉ ✗
```

---

## 🚀 Installation

### Prérequis

- Python 3.9+
- Compte Groq (gratuit) : [https://console.groq.com](https://console.groq.com)

### Étapes

```bash
# 1. Cloner le repository
git clone <votre-repo>
cd ai_dev_team

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'API Key
cp .env.example .env
# Éditer .env et ajouter votre GROQ_API_KEY

# 4. Lancer l'application
streamlit run app.py
```

L'application s'ouvrira automatiquement sur `http://localhost:8501`

---

## 📖 Utilisation

### 1. Configuration

- Entrez votre **Groq API Key** dans la sidebar
- (Optionnel) Uploadez des **PDFs** de documentation technique

### 2. Décrivez votre besoin

Exemples :
```
"Créer un script Python qui récupère les données météo d'une ville 
via l'API OpenWeatherMap, gère les erreurs réseau, et sauvegarde 
les résultats dans un fichier CSV."
```

```
"Implémenter un client pour l'API GitHub qui récupère les repos 
d'un utilisateur avec authentification et pagination."
```

### 3. Lancez l'équipe

Cliquez sur **🚀 Lancer l'équipe** et observez les agents travailler en temps réel !

### 4. Téléchargez le résultat

Récupérez un **ZIP** contenant :
- `main.py` - Code principal
- `test_main.py` - Tests unitaires
- `README.md` - Documentation
- `requirements.txt` - Dépendances

---

## 🧠 Techniques de Raisonnement

### Chain of Thought (CoT) - Product Owner

Le PO décompose l'analyse étape par étape :

```
Étape 1 : Comprendre le besoin métier
Étape 2 : Identifier les fonctionnalités principales
Étape 3 : Décomposer en User Stories
Étape 4 : Définir les critères d'acceptation
```

### ReAct (Reason + Act) - Developer

Le Dev alterne entre pensée et action :

```
PENSÉE : "J'ai besoin de faire des requêtes HTTP"
ACTION : import requests
OBSERVATION : "Le PDF mentionne une authentification Bearer"
PENSÉE : "Je dois ajouter un header Authorization"
ACTION : Ajouter le code d'authentification
```

### Self-Correction - QA Engineer

Le QA critique sa propre analyse :

```
ANALYSE INITIALE : "Le code semble correct"
AUTO-CRITIQUE : "Attendez... il n'y a pas de gestion d'erreur"
CORRECTION : "Il faut ajouter try/except et un timeout"
```

### Tree of Thoughts (ToT) - Tech Lead

Le Tech Lead explore plusieurs options avant de décider :

```
Option A : Valider en l'état (7/10)
Option B : Demander corrections mineures (9/10) ✓
Option C : Rejeter complètement (2/10)

DÉCISION : Option B retenue
```

---

## 📂 Structure du Projet

```
ai_dev_team/
├── app.py                      # Application Streamlit principale
├── orchestrator.py             # Coordinateur des agents
├── requirements.txt            # Dépendances
├── .env.example               # Template de configuration
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Classe abstraite
│   ├── product_owner.py       # Agent PO (CoT)
│   ├── developer.py           # Agent Dev (ReAct)
│   ├── qa_engineer.py         # Agent QA (Self-Correction)
│   └── tech_lead.py           # Agent Tech Lead (ToT)
└── utils/
    ├── __init__.py
    └── pdf_processor.py       # Traitement PDFs avec RAG
```

---

## 🎯 Cas d'Usage

### 1. Développement Rapide
*"J'ai besoin d'un script en 5 minutes"*

→ Décrivez le besoin, l'équipe génère le code et les tests

### 2. Apprendre en Observant
*"Comment structurer un client API ?"*

→ Observez le raisonnement du Developer et les critiques du QA

### 3. Prototypage
*"Tester une idée rapidement"*

→ Uploadez une spec PDF, obtenez un prototype fonctionnel

---

## 🔧 Technologies Utilisées

- **Streamlit** : Interface utilisateur
- **LangChain** : Framework pour agents
- **Groq** : API LLM (LLaMA 3.1 70B gratuit)
- **HuggingFace** : Embeddings pour RAG (gratuit)
- **ChromaDB** : Base vectorielle pour les PDFs
- **PyPDF** : Parsing de documents


---

## 🚧 Limitations Connues

⚠️ **API Rate Limiting** : Groq gratuit a des limites (20 req/min)  
⚠️ **Complexité du code** : Optimisé pour scripts moyens (<300 lignes)  
⚠️ **Langages supportés** : Python uniquement pour l'instant  
⚠️ **PDFs** : Fonctionnent mieux avec des documents textuels (pas de scan d'images)  

---


---

## 👥 Contributeurs

- **Arthur** - Développeur principal

---

## 📝 Licence

Ce projet est réalisé dans un cadre académique.

---

## 🙏 Remerciements

- **Anthropic** pour Claude (inspiration du naming)
- **Groq** pour l'API gratuite
- **LangChain** pour le framework
- **Streamlit** pour l'interface

---

<div align="center">

**Fait avec ❤️ et beaucoup de prompts**

[⭐ Star ce projet](https://github.com/votre-repo) | [🐛 Reporter un bug](https://github.com/votre-repo/issues)

</div>
