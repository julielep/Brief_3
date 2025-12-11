*Architecture :*

projet/
├── backend/

│   ├── API/

│   │   ├── BD_api.py

│   │   └── sentiment_api.py

│   │

│   ├── modules/

│   │   ├── df_tools.py

│   │   └── sentiment_tools.py

│   │
│   └── data/
│       └── DB_quotes.db
│
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── 0_Insert_quote.py
│       ├── 1_Afficher.py
│       └── 2_Recherche.py
│
├── README.md
├── .venv/
└── .gitignore

Ma base de données "quotes_db.csv"
|Citation |
|:--------|
|ID       |
|text     |


### Commandes
- Démarrage des serveurs uvicorn :
```bash
python -m backend.API.sentiment_api
python -m backend.API.BD_api
```
- Lancement de streamlit :
```bash
streamlit run .\frontend\APP\app.py   
```
