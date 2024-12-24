from chroma_service import ChromaService
from fastapi import FastAPI

from config import Config
from models.query_input_request import Question
from models.upload_data_request import UploadDataRequest
from openai_service import OpenAI
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
    context = "\n".join([doc.page_content for doc in results])
    
    prompt = f"""
    you are a assistance to answer questions. Use the following context to answer the question 
    You can not use external information. Use markdown to format your answer. If you can not answer the question,
    please say you don't know the answer.
    You have a 100 word limit.
    
    Context: 
    {context}
    
    question: {question.question}
    """
    
    output = OpenAI.gpt.invoke(prompt)
    print(output)
    return output.content

