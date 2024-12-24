
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from config import Config


class OpenAI:

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",
                                  api_key=Config.OPEN_AI_KEY)
    
    gpt = ChatOpenAI(model="gpt-4o", api_key=Config.OPEN_AI_KEY)
