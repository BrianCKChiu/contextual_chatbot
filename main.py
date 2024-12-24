from chroma_service import ChromaService
from fastapi import FastAPI

from config import Config
from models.query_input_request import Question
from models.upload_data_request import UploadDataRequest
from utils.recursive_splitter import RecursiveSplitter
from utils.extract_text_file_contents import extract_text_file_contents

_ = Config()


ACCEPTABLE_FILE_TYPES = ["plain/text"]
app = FastAPI(on_startup=[ChromaService.initialize_client])


@app.post("/uploadFile")
async def upload_file(request: UploadDataRequest):
    if request.file.content_type not in ACCEPTABLE_FILE_TYPES:
        raise Exception("Invalid file type, only plain text files are accepted")

    data = await extract_text_file_contents(request.file)

    chunks = RecursiveSplitter.split_content(content=data)
    ChromaService.add_chunks(chunks, request.meta_data)



@app.post("/query")
async def query(question: Question):
    results = ChromaService.query(query_text=question.question)
    print(results)

