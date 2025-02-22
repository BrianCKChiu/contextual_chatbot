from typing import List
from uuid import uuid4
from chromadb import PersistentClient
from langchain_core.documents import Document
from langchain_chroma import Chroma
from config import Config
from services.openai_service import OpenAiService


def ensure_initialized(method):
    def wrapper(self, *args, **kwargs):
        if self.client is None:
            raise Exception("Chroma Service not initialized properly")
        return method(self, *args, **kwargs)

    return wrapper


class ChromaService:

    vector_store = None
    client = None

    @classmethod
    def initialize_client(self):
        self.client = PersistentClient(Config.CHROMA_DATABASE_DIR)
        self.vector_store = Chroma(
            collection_name="test_collection",
            client=self.client,
            embedding_function=OpenAiService.embeddings,
        )

    @classmethod
    @ensure_initialized
    def add_chunks(self, chunks: List[str], meta_data: dict = {}):
        uuids: List[str] = []
        documents = []

        for _, chunk in enumerate(chunks):
            uuids.append(str(uuid4()))
            documents.append(Document(page_content=chunk, meta_data=meta_data))

        self.vector_store.add_documents(
            documents=documents,
            ids=uuids,
            embeddings=[
                OpenAI.embeddings,
            ],
        )

    @classmethod
    @ensure_initialized
    def query(self, query_text: str, meta_data: dict[str, str] = {}) -> List[Document]:

        docs = self.vector_store.similarity_search(query=query_text, filter=meta_data)
        return docs
