from pydantic import BaseModel


class UserMessageRequest(BaseModel):
    chat_id: str
    message: str
