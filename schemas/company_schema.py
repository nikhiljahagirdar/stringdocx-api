from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl


class CompanyBase(BaseModel):
    id: Optional[int] = None
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    company_website: Optional[HttpUrl] = None
    logo: Optional[str] = None
    subscription_id: Optional[int] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    pass


class Company(CompanyBase):
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
