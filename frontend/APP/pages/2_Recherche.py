import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
load_dotenv()

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"
API_ROOT_URL_IA = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT_IA', '9080')}"
API_URL_IA = API_ROOT_URL_IA + "/analyse_sentiment/"

st.title("Lire une citation")

st.subheader("Citation par ID")
API_URL = API_ROOT_URL + "/read/"
API_URL_IDX = API_ROOT_URL + "/read/idx/"

try:
    idx_response = requests.get(API_URL_IDX)
    if idx_response.status_code == 200:
        ids = [int(item["id"]) for item in idx_response.json()]
    else:
        st.error(f"Erreur API : {idx_response.status_code}")
except requests.exceptions.ConnectionError:
    st.error(f"Impossible de se connecter à l'API à {API_URL}")

with st.form("search_by_id"):
    quote_id = st.selectbox("Choisissez un ID :", ids)
    submitted = st.form_submit_button("Rechercher")

if submitted:
    try:
        response = requests.get(API_URL + str(quote_id))
        if response.status_code == 200:
            result = response.json()
            st.session_state.quote = result.get("text", "")
            st.success(f"Citation {quote_id}")
            st.info(st.session_state.quote)
    except requests.exceptions.ConnectionError:
        st.error(f"Impossible de se connecter à l'API à {API_URL}")

# ---- Analyse des sentiments ----
if "quote" in st.session_state and st.session_state.quote:
    if st.button("Analyser les sentiments de la citation"):
        if st.session_state.quote:
            data = {"text": st.session_state.quote}
            try:
                response = requests.post(API_URL_IA, json=data)
                if response.status_code == 200:
                    sentiment = response.json()
                    st.write("Résultats de l'analyse :")
                    st.write(f"Polarité négative : {sentiment['neg']}")
                    st.write(f"Polarité neutre : {sentiment['neu']}")
                    st.write(f"Polarité positive : {sentiment['pos']}")
                    st.write(f"Score composé : {sentiment['compound']}")
                    if sentiment['compound'] >= 0.05 :
                        st.write("Sentiment global : Positif 😀")
                    elif sentiment['compound'] <= -0.05 :
                        st.write("Sentiment global : Négatif 🙁")
                    else :
                        st.write("Sentiment global : Neutre 😐")
                        logger.info(f"Résultats affichés: {sentiment}")

                    st.balloons()
                else:
                    st.error(f"Erreur API : {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")
                logger.error(f"Erreur de connexion à l'API : {e}")
            except Exception as e :
                st.error(f"Une erreur est survenue: {e}")
                logger.error(f"Une erreur est survenue: {e}")
        else:
            st.write("Veuillez entrer du texte pour l'analyse.")
