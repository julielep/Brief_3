#/backend/modules/sentiment_tools.py
import os
from nltk.sentiment import SentimentIntensityAnalyzer

DB_FILE = os.path.join("backend", "data", "DB_quotes.db")

def give_sentiment(text: str) -> dict:
    """Donne le sentiment à partir da la citation en anglais."""
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment  
