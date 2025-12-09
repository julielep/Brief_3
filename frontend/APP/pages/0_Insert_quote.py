#frontend/pages/0_insérer.py
import streamlit as st
import requests
import os
import pandas as pd

from lingua import Language, LanguageDetectorBuilder

# Crée le détecteur de langue
detector = LanguageDetectorBuilder.from_all_languages().build()

from dotenv import load_dotenv
load_dotenv()
API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}" 
API_URL = API_ROOT_URL + "/insert"

API_ROOT_URL_IA =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT_IA', '8080')}"
API_URL_IA =  API_ROOT_URL_IA + "/analyse_sentiment/"

st.title("Insérer une nouvelle citation !")

with st.form("insert_form"):

    new_quote_texte = st.text_area('Texte de la citation en anglais :', height=150)

    submitted = st.form_submit_button("Ajouter la citation")

    if submitted:
        #On vérifie que le texte n'est pas vide ou ' ':
        if not new_quote_texte or new_quote_texte.strip() == '':
            st.error("La citation ne peut pas être vide.")
            st.stop() #Pour ne pas continuer l'éxécution du code
        language = detector.detect_language_of(new_quote_texte)
        if language == Language.ENGLISH:
            #récupère le texte si non vide
            data = {"text": new_quote_texte}
            #écrire une info si ça prend du temps
            st.info("➿Envoie à l'API")

            try:
                response = requests.post(API_URL, json = data) #attention au format
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success(f"Citation ajoutée ! ID: ")
                    st.balloons()
                    
                else: 
                    st.error(f"Erreur de l'API avec le code {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error(f"ERREUR : impossible de se connecter à l'API à {API_ROOT_URL}")
                st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
        else:
            st.error(f"Le texte n'est pas en anglais, il ne peut pas être ajouté.")
            st.stop()


