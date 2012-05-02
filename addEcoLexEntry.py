## Matthias Orlowski
## 04/29/2012
## Script to store entries at ecolex.org to a database

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:////ecolex.db', echo=True)
Base = declarative_base()

class EcoLexEntry(Base):
    __tablename__ = 'ecolexentry'

    id = Column(Integer,primary_key=True)
    ecolex_id = Column(String) # unique = True, Legislation ID number
    name = Column(String) # Title of text
    country = Column(String) # Country
    date = Column(String) # Date of text
    legtype = Column(String) # Type of document
    source = Column(String) # Source
    fulltext = Column(String) # Link to full text
    keywords = Column(String) # Keywords original
    abstract = Column(String) # Abstract original
    language = Column(String) # language of data base entries
    abstractEN = Column(String) # Keywords english
    keywordsEN = Column(String) # Abstract english

    def __init__(self,entry):

        self.ecolex_id = entry.ecolex_id
        self.name = entry.name
        self.country = entry.country
        self.date = entry.date
        self.legtype = entry.legtype
        self.source = entry.source
        self.fulltext = entry.fulltext
        self.keywords = entry.keywords
        self.abstract = entry.abstract
        self.language = entry.language
        self.abstractEN = entry.abstractEN
        self.keywordsEN = entry.keywordsEN

    def __repr__(self):
        return "<Law('%s', '%s')>" % (self.ecolex_id, self.name)


def createDataBase():
    """Creates tables if not existant."""
    Base.metadata.create_all(engine) 


def addEntry(entry,first):
    """Passes a scraped law object to the database."""
    enter = EcoLexEntry(entry)
    if first == True:
        createDataBase()
    session = startSession()
    session.add(enter)
    session.commit()

def startSession():
    """Starts session for interaction with database."""
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    
# toDo
# implement checking for uniquenes of lex ids
# change field type types to appropriate types: f.i. text instead of string since the latter takes only a limited number of characters
# change data base to utf-8 data base and generally use utf-8 encoding 
