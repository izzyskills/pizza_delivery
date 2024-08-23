from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import PostgresDsn
from config import setting

# add you database according to username,port,pwd,hostname and db

database_url = PostgresDsn.build(
    scheme="postgresql",
    user=setting.db_usr,
    password=setting.db_pwd,
    host=setting.db_host,
    path=f"/{setting.db_name}",
)

engine = create_engine(str(database_url), echo=True)


Base = declarative_base()

Session = sessionmaker()
