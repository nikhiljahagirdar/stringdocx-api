from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GetUser(BaseModel):
    id: Optional[int]
    email: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    firstname: str
    lastname: str
    role: str
    subscription_id: Optional[int] = None
    company_id: Optional[int] = None
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None


class CreateUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[str] = "user"
    subscription_id: Optional[int] = None
    company_id: Optional[int] = None
    billingCycle: Optional[str] = "yearly"
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None


class GetUserPassword(BaseModel):
    id: Optional[int]
    email: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    firstname: str
    lastname: str
    password_hash: str
    role: str
    subscription_id: Optional[int] = None
    company_id: Optional[int] = None
    company_id: Optional[int] = None
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None
