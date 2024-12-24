
from langchain_openai import OpenAIEmbeddings
from config import Config


class OpenAI:

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",
                                  api_key=Config.OPEN_AI_KEY)
