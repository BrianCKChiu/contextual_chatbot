from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from config import Config

engine = create_engine(Config.SQLITE_CONNECTION_URI)
Base = declarative_base()

LocalSqlSession = sessionmaker(engine, expire_on_commit=False)
