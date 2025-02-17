from services.chroma_service import ChromaService
from fastapi import FastAPI
from routers.contextual_bot import contextual_bot_router
from config import Config


_ = Config()
app = FastAPI(on_startup=[ChromaService.initialize_client])

app.include_router(contextual_bot_router.router)
