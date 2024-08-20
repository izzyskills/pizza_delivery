import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

load_dotenv()

database_url = os.getenv("Database_Url")
engine = create_engine(str(database_url), echo=True)


Base = declarative_base()

Session = sessionmaker()
