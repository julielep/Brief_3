# backend/API/sentiment_api.py

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from loguru import logger
from backend.modules.sentiment_tools import give_sentiment

load_dotenv()

# --- Pydantic models ---
class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    neg: float
    neu: float
    pos: float
    compound: float

app = FastAPI(title="API_IA")
logger.add("logs/sentiment_api.log", rotation="500 MB", level="INFO")

@app.get("/")
def root():
    return {"Hello": "world", "status": "API is running"}

@app.post("/analyse_sentiment/", response_model=SentimentResponse)
def analyse_sentiment(request: TextRequest):
    """Analyse les sentiments"""
    try:
        result = give_sentiment(request.text)
        logger.info(f"Texte : '{request.text}'. Résultats: {result}")
        return {
            "neg": result["neg"],
            "neu": result["neu"],
            "pos": result["pos"],
            "compound": result["compound"]}

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))

   
if __name__ == "__main__": 
    try:
        port = os.getenv("FAST_API_PORT_IA", "9080")
        url = os.getenv("API_BASE_URL")
        port = int(port)

    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run("backend.API.sentiment_api:app", 
                host = url, 
                port = port, 
                reload = True) 