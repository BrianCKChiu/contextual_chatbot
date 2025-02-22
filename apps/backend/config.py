import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY")
    CHROMA_DATABASE_DIR = os.environ.get("CHROMA_DATABASE_DIR")
    SQLITE_CONNECTION_URI = os.environ.get("SQLITE_CONNECTION_URI")
