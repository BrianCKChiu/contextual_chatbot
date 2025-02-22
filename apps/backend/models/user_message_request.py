from pydantic import BaseModel


class UserMessageRequest(BaseModel):
    message: str
