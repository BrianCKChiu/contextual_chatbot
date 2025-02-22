from services.sqlite_service import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class Chat(Base):
    __tablename__ = "chat"
    id: Mapped[str] = mapped_column(primary_key=True)
    title = Mapped[Optional[str]]
    last_message_at = Mapped[Optional[int]]
