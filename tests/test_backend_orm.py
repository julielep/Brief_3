#tests/test_backend_orm.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
from fastapi.testclient import TestClient

from backend.API.BD_api import app
from backend.modules.db_tools import write_db, read_db, Base
from backend.modules.sentiment_tools import give_sentiment
"""
On veut tester la base de données sans faire intervenir la base de donnée qui existe déjà.
On va donc créer une BDD virtuelle.

Pour faire les tests bien faire attention au type de variable en entrée et en sortie. 
"""
#-------------------
#------FIXTURE------
#-------------------
##Create engine
@pytest.fixture(scope="module")
def engine_test():
    """Create engine"""
    return create_engine("sqlite:///:memory:") #base de donnée en mémoire -> virtuelle

##Create DB
@pytest.fixture(scope='module')
def setup_db(engine_test): #quand on l'apelle il sait qu'on doit appeler @pytest.fixture qui a été transormé en module -> pas besoin de parenthèse
    """Create table"""
    #ici le engine_test correspond à la fonction créer au dessus 
    #Création de la base de données
    Base.metadata.create_all(engine_test) 
    yield #Permet de continuer la boucle tous en faisant un return
    Base.metadata.drop_all(engine_test) #Une fois qu'on a finis de se servie de la BDD elle se vide -> on ne la garde pas en mémoire

##Create DB session
@pytest.fixture(scope='function')
def db_session(engine_test, setup_db): #on met setup_db sans l'utiliser -> il voit qu'on l'utilise et créer la BDD automatiquement sans qu'on le précise
    """Yield DB session"""
    connection = engine_test.connect() #Connecte le moteur
    transaction = connection.begin() #Démarre la transaction

    SessionTest = sessionmaker(bind=engine_test, autocommit=False, autoflush=False) #Fait notre session
    session = SessionTest(bind=connection) #On se connecte à la session 

    yield session
    #Clean
    session.close() #ferme la session
    transaction.rollback() #Annule les derniers commit
    connection.close() #ferme la connexion


#-------------------
#-------MOCK--------
#-------------------
##OVERRIDE SESSION LOCAL 
@pytest.fixture(autouse=True) #On laisse pytest gérer tout seul
def override_get_db_session(monkeypatch, db_session): #monkeypatch appartient à pytest et permet de patcher ??
    """Mock get db session"""
    def mock_get_db_session(): #qd dans le code il y a db_session, il va prendre notre db_session ici 
        return db_session
    #Pour dire où ? on utilise monkeypatch
    monkeypatch.setattr('backend.modules.db_tools.get_db_session', mock_get_db_session)



#-------------------
#-------TEST--------
#-------------------
#Test write_db and read_db
def test_add_read_and_read_quote():
    quote = 'test'
    dico = {"text": [quote]}
    df = pd.DataFrame(dico)
    #add citation
    write_db(quote)
    #read citation
    df2 = read_db() 
    citation = df2.iloc[0]['text']
    assert not df2.empty
    assert citation == quote

def test_sentiment():
    quote = 'Happy'
    sentiment = give_sentiment(quote)
    assert sentiment['pos'] > 0.5
    








