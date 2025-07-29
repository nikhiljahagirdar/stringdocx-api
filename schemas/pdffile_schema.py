from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PDFFileCreate(BaseModel):
    user_id: Optional[int]
    filename: str
    path: str
    size: int
    original_filename: str
    processed_filename: Optional[str] = None
    processed_path: Optional[str] = None
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    status: Optional[str] = ""
    status_message: Optional[str] = ""

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class PDFFileRead(PDFFileCreate):
    id: int
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
