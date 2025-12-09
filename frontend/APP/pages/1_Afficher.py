# frontend/pages/0_insérer.py
import streamlit as st
import requests 
import os 
import pandas as pd
from dotenv import load_dotenv 

load_dotenv()

API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"
API_URL =  API_ROOT_URL + "/read"

API_ROOT_URL_IA =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT_IA', '8080')}"
API_URL_IA =  API_ROOT_URL_IA + "/analyse_sentiment/"

st.title("Lire toutes les citations")

import streamlit as st

if st.button("Charger les données 📚", type='primary'):
    st.info("Lire depuis l'API")

    try : 
        response = requests.get(API_URL)

        if response.status_code == 200:
            result = response.json()

            df = pd.DataFrame(result)
            st.dataframe(df, width="stretch")

            st.success("Lecture de toutes les citations")
            st.balloons()
        else:
            st.error(f"Erreur de l'API avec le code {response.status_code}")


    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")