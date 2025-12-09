# backend/modules/db_tools.py
import pandas as pd
import os
from loguru import logger
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker

DB_FILE = os.path.join("backend", "data", "DB_quotes.db")

#Création de la base de données :
Base = declarative_base()

class Citation(Base):
    __tablename__ = 'citations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)

class Sentiment(Base):
    __tablename__ = 'sentiments'
    id = Column(Integer, primary_key = True, autoincrement=True)
    negatif = Column(Float)
    neutre = Column(Float)
    positif = Column(Float)
    combine = Column(Float)
    id_citation = Column(Integer, ForeignKey(Citation.id))


    
#Connection à la base de données
def Connect_session():
    """Connexion à la base SQLite et renvoie la session"""
    engine = create_engine(f"sqlite:///{DB_FILE}", echo=False) #Echo=False pour éviter d'avoir les sorties SQL dans le terminal
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def write_db(texte : str):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True) #Vérifie que le path existe sinon il en créer un 
    session = Connect_session()
    CITATION = Citation(text = texte[0]) #On récupère la citation saisie dans streamlit
    session.add(CITATION)
    session.commit()
    session.close()
    print("Utilisateur ajouté avec succès.")


def read_db()->pd.DataFrame: 
    with Connect_session() as session:
        texte = session.query(Citation).all() 
    data = [{"id": t.id, "text": t.text} for t in texte]
    return pd.DataFrame(data)


def initialize_db():
    if os.path.exists(DB_FILE):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DB_FILE}")
        df = pd.DataFrame(columns=['id', 'text'])
        df = df.set_index('id')
        write_db(df)
        logger.info(f"le fichier {DB_FILE} a été créé")