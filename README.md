# PDF-Assistant

Assistant IA de Lecture de Documents PDF avec LangChain, FastAPI et déploiement EC2.

## Fonctionnalités

- Chargement et découpage de documents PDF
- Embeddings via OpenAI et indexation vectorielle avec FAISS
- Assistant conversationnel avec mémoire contextuelle (LangChain)
- API REST `/ask` sécurisée avec un token (Bearer)
- Déploiement sur instance EC2 (Ubuntu 24.04)

## Structure du projet

my-pdf-assistant/
├── api.py              # API FastAPI exposant le point /ask
├── main.py             # Traitement PDF, embeddings, chaîne LangChain
├── requirements.txt    # Dépendances
├── .env                # Variables secrètes (API_TOKEN, OPENAI_API_KEY)
├── pdfs/               # Fichiers PDF à charger
│   ├── Conditions_Generales_2025_AAV.pdf
│   └── DIP_AAV_2025.pdf
└── README.md

## Installation locale

bash
git clone https://github.com/VioletaBD/PDF-Assistant.git
cd my-pdf-assistant
python3 -m venv venv
venv\Scripts\activate sur Windows
pip install -r requirements.txt

Ajouter un fichier `.env` :

API_TOKEN=chatbot_dojo_pdf_assistant_123456
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

## Lancer le serveur

bash
uvicorn api:app --host 0.0.0.0 --port 8000

---

## Interroger l'API

bash
curl -X POST http://<EC2-IP>:8000/ask \
  -H "Authorization: Bearer chatbot_dojo_pdf_assistant_123456" \
  -H "Content-Type: application/json" \
  -d '{ "question": "Quels sont les risques assurés ?" }'

---

## Accès Swagger

http://<EC2-IP>:8000/docs


## Déploiement EC2

- Instance Ubuntu 24.04 avec port 8000 ouvert
- Accès SSH via clé `.pem`
- Uvicorn lancé manuellement

---

## Licence

MIT – libre d'utilisation pour vos projets Dojo ou personnels.
