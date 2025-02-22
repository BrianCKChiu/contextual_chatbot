from pydantic import BaseModel
from typing import Optional


class NewChatRequest(BaseModel):
    message: str
    model: Optional[str] = "gpt-4o"
