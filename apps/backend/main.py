from services.chroma_service import ChromaService
from fastapi import FastAPI
from routers import chat_router
from config import Config


_ = Config()
app = FastAPI(on_startup=[ChromaService.initialize_client])

app.include_router(chat_router.router)
