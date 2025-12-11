#tests/test_backend_api.py
from fastapi.testclient import TestClient

from backend.API.BD_api import app
from backend.API.sentiment_api import app as app_ia

client = TestClient(app) 
client2 = TestClient(app_ia)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_root_ia():
    response = client2.get("/")
    assert response.status_code == 200

def test_post():
    response = client.post("/insert/", json={"text": "test"})
    assert response.status_code == 200

def test_post_ia():
    response = client2.post("/analyse_sentiment/", json={"text": "test"})
    assert response.status_code == 200












