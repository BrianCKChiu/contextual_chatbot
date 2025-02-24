from enum import Enum
from pydantic import BaseModel
from services.sqlite_service import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum, String, Integer, ForeignKey
from models.chat import Chat


class ChatRole(str, Enum):

    USER = "user"
    ASSISTANT = "assistant"


class ChatRecord(Base):
    __tablename__ = "chatRecord"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    message: Mapped[str] = mapped_column(String)
    role: Mapped[ChatRole] = mapped_column(SAEnum(ChatRole))
    datetime: Mapped[int] = mapped_column(Integer)
    chat_id: Mapped["Chat"] = mapped_column(String, ForeignKey("chat.id"))

    chat: Mapped[Chat] = relationship("Chat")


class ChatRecordSchema(BaseModel):
    message: str
    role: ChatRole
