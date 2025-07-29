# schemas/pdf_master_config_schema.py

from pydantic import BaseModel
from typing import Optional


class PdfMasterConfigCreate(BaseModel):
    configType: str
    configName: str
    configValue: str
    configDescription: Optional[str] = None
    
    isChild: Optional[bool] = False


class PdfMasterConfigRead(PdfMasterConfigCreate):
    id: int
    createdOn: str
    updatedOn: Optional[str]
