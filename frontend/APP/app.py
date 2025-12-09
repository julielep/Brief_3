# frontend/app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv 

load_dotenv()
API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}" #Le mieu est de le déclarer dans un fichier variable d'environnenment
API_ROOT_URL_IA = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT_IA', '9080')}"
st.title("Connexion aux API")
st.subheader("Vérification de l'API")

#--- Le bouton ---
if st.button("Ping l'API DB (Route /)"):
    try:
        #1. Requête GET (pour lire, recevoir) vers la route principale
        response = requests.get(API_ROOT_URL)

        #2. Si résultat -> il faut l'afficher
        if response.status_code == 200: #ça se passe bien -> code 200 le code fonctionne (https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP)
            st.success("Connexion réussi à l'API FastAPI")
            st.code(f"statut HTTP : {response.status_code}")

            st.json(response.json()) #Récupère la réponse json de la réponse
        
        else:
            st.error(f"L'API a répondu avec une erreur : {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        st.error(f"ERREUR : impossible de se connecter à l'API à {API_ROOT_URL}")
        st.warning("Veuillez vous assurez que le serveur Uvicorn est bien lancer en arrière plan.")


#--- Le bouton ---
if st.button("Ping l'API IA (Route /)"):
    try:
        #1. Requête GET (pour lire, recevoir) vers la route principale
        response = requests.get(API_ROOT_URL_IA)

        #2. Si résultat -> il faut l'afficher
        if response.status_code == 200: #ça se passe bien -> code 200 le code fonctionne (https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP)
            st.success("Connexion réussi à l'API FastAPI")
            st.code(f"statut HTTP : {response.status_code}")

            st.json(response.json()) #Récupère la réponse json de la réponse
        
        else:
            st.error(f"L'API a répondu avec une erreur : {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        st.error(f"ERREUR : impossible de se connecter à l'API à {API_ROOT_URL_IA}")
        st.warning("Veuillez vous assurez que le serveur Uvicorn est bien lancer en arrière plan.")