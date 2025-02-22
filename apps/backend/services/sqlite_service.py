from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SqliteService:
    engine = create_engine(Config.SQLITE_CONNECTION_URI)
    LocalSqlSession = sessionmaker(engine, expire_on_commit=False)

    @classmethod
    async def init_db(self):
        Base.metadata.create_all(self.engine)


def get_conn():
    db = SqliteService.LocalSqlSession()
    try:
        yield db
    finally:
        db.close()
