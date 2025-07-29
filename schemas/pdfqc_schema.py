from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PDFQCCreate(BaseModel):
    doc_id: int
    is_security: Optional[bool] = False
    is_encrypted: Optional[bool] = False
    has_bookmarks: Optional[bool] = False
    has_tags: Optional[bool] = False
    has_media: Optional[bool] = False
    has_images: Optional[bool] = False
    has_fonts: Optional[bool] = False
    has_tables: Optional[bool] = False
    has_links: Optional[bool] = False
    has_annotations: Optional[bool] = False
    has_form_fields: Optional[bool] = False
    

class PDFQCRead(PDFQCCreate):
    doc_id: int
    filename: str
    filepath: str
    status: str
    is_security: Optional[bool] = False
    is_encrypted: Optional[bool] = False
    has_bookmarks: Optional[bool] = False
    has_tags: Optional[bool] = False
    has_media: Optional[bool] = False
    has_images: Optional[bool] = False
    has_fonts: Optional[bool] = False
    has_tables: Optional[bool] = False
    has_links: Optional[bool] = False
    has_annotations: Optional[bool] = False
    has_form_fields: Optional[bool] = False
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None
