from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.content_splitter import ContentSplitter


class RecursiveSplitter(ContentSplitter):

    def split_content(content: str) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n", ".", " "],
            chunk_size=500,
            chunk_overlap=100,
        )

        return splitter.split_text(content)
