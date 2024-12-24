from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class UploadDataRequest(BaseModel):
    file: UploadFile
    meta_data: Optional[dict[str, str]] = {}
