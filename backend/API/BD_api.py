#backend/BD_api.py
import uvicorn
import os
import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
load_dotenv()

from backend.modules.db_tools import initialize_db, read_db, write_db


#Modèle pydantic

class QuoteRequest(BaseModel): 
    text : str  

class QuoteResponse(BaseModel): 
    id : int
    text : str

class IDresponse(BaseModel): 
    id : int   

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}" 

#--- Création si besoin de la base de données ---
initialize_db()

# --- Configuration ---
app = FastAPI(title='API')

@app.get("/") 
def read_root(): 
    """Vérifie que la root fonctionne."""
    return {"Hello": "world", "status": "API is running"}

@app.post("/insert/", response_model=QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """Insère une nouvelle citation."""
    df = read_db()
    if df.empty:
        new_id = 1
    elif df.index.max() <= 0:
        new_id = 1
    else :
        new_id = 1 + df.index.max()

    objet = {"text": [quote.text]}  
    write_db(objet['text'][0])
    return {"id": new_id, "text": quote.text} 

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    """Lire toute les citations."""
    df = read_db()
    return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')

@app.get("/read/{id}", response_model=QuoteResponse)
def read_specific_quotes(id : int):
    """Lire la citation pour un ID donné."""
    df = read_db()
    if id not in df.index:
        raise HTTPException(status_code=404, detail=f"Citation avec ID {id} non trouvée")
    quote_data = df.loc[id].to_dict()
    quote_data['id'] = id
    return quote_data

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    """Lire la citation d'un ID pris au hasard"""
    df = read_db()
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation aléatoire non trouvée")
    
    random_id = random.choice(df.index)
    quote_data = df.loc[random_id].to_dict()
    quote_data['id'] = random_id

    return quote_data

@app.get("/read/idx/", response_model=list[IDresponse])
def read_idx():
    """Retourne tous les ID de la base de donnée."""
    df = read_db()
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    return [{"id": int(i)} for i in df.index]



if __name__ == "__main__": 
    try:
        port = os.getenv("FAST_API_PORT", "8080")
        url = os.getenv("API_BASE_URL")
        port = int(port)

    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run("backend.API.BD_api:app", 
                host = url, 
                port = port, 
                reload = True)