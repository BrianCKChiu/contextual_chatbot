from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import uuid4


from services.chroma_service import ChromaService
from services.sqlite_service import get_conn
from services.openai_service import OpenAiService

from utils.recursive_splitter import RecursiveSplitter
from utils.extract_text_file_contents import extract_text_file_contents

from models.contracts.user_message_request import UserMessageRequest
from models.contracts.upload_data_request import UploadDataRequest
from models.chat import Chat


router = APIRouter(prefix="/contextual_bot", tags=["contextual_bot"])
ACCEPTABLE_FILE_TYPES = ["plain/text"]


@router.post("/uploadFile")
async def upload_file(request: UploadDataRequest):
    if request.file.content_type not in ACCEPTABLE_FILE_TYPES:
        raise Exception("Invalid file type, only plain text files are accepted")

    data = await extract_text_file_contents(request.file)

    chunks = RecursiveSplitter.split_content(content=data)
    ChromaService.add_chunks(chunks, request.meta_data)


@router.post("/chat")
async def chat(request: UserMessageRequest, db_conn: Session = Depends(get_conn)):
    message = request.message

    return StreamingResponse(
        content=OpenAiService().stream_chat_completion(user_message=message),
        media_type="text/event-stream",
    )


@router.post("/new-chat")
async def start_chat(db_conn=Depends(get_conn)):
    chat_id = str(uuid4())
    chat = Chat(id=chat_id)
    db_conn.add(chat)
    db_conn.commit()
    return {"chat_id": chat_id}


@router.post("/query")
async def query(request: UserMessageRequest):
    question = request.message
    results = ChromaService.query(query_text=question)
    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
    you are a assistance to answer questions. Use the following context to
    answer the question. You can not use external information. Use markdown
    to format your answer. If you can not answer the question,
    please say you don't know the answer.
    You have a 100 word limit.

    Context:
    {context}

    question: {question.question}
    """

    output = OpenAiService.gpt.invoke(prompt)
    print(output)
    return output.content
