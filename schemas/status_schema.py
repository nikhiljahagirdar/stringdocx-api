from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SiteStatusCreate(BaseModel):
    """
    Pydantic model for creating a new site status entry.
    """
    status_type: str
    status_message: str
    pdf_file_id: Optional[int] = None


class SiteStatusRead(BaseModel):
    """
    Pydantic model representing the 'sitestatus' table.
    """
    id: Optional[int] = None
    status_type: str
    status_message: str
    pdf_file_id: Optional[int] = None
    createdon: Optional[datetime] = None
    updatedon: Optional[datetime] = Field(None, description="Update timestamp")
    
