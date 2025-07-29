from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PdfUserConfigCreate(BaseModel):
    config_id: int
    user_id: int
    doc_id: int


class PdfUserConfigRead(PdfUserConfigCreate):
    id: int
    created_on: str
    updated_on: Optional[str]