
from fastapi import UploadFile, File


async def extract_text_file_contents(file: UploadFile = File(...)) -> str:
    content = await file.read()
    return content.decode("utf-8")
