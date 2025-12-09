Installation des bibliothèques
pip install fastapi uvicorn

Un mini programme complet:

frontend (streamlit)
backend:
modules (contenir nos propres modules)
data (nos csv)
Architecture
mon projet/
├─────backend
│   ├───modules
│   │    └── df_tools.py
│   ├───data
│   │    └── quotes_db.csv
│   │    └── DB_quotes.db
│   └── main.py
│   
├───frontend
│   ├──app.py
│   └──pages 
│       ├─0_insérer.py
│       ├─1_Afficher.py
│       ├─2_rechercher.py
├─README.md
├─.venv
└─.gitignore
Ma base de données "quotes_db.csv"
Colonnes :

id
text
Commande pour lancer le serveur uvicorn
uvicorn backend.main:app --reload --log-level debug
debug pour afficher les log dans le terminal