from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# add you database according to username,port,pwd,hostname and db


engine = create_engine(str(settings.db_url), echo=True)


Base = declarative_base()

Session = sessionmaker()
