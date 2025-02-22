from services.chroma_service import ChromaService
from fastapi import FastAPI
from routers import chat_router
from config import Config
from services.sqlite_service import SqliteService


_ = Config()


app = FastAPI(on_startup=[ChromaService.initialize_client, SqliteService.init_db])


app.include_router(chat_router.router)
