from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id: Optional[int]
    firstname: str
    lastname: str
    email: str
    subscription_id: Optional[int] = 4
    role: str


class TokenData(BaseModel):
    email: Optional[str] = None


class GoogleAuth(BaseModel):
    token: str


class Login(BaseModel):
    email: str
    password: str


class Register(BaseModel):
    account_type: str
    firstname: str
    lastname: str
    email: str
    password: str
    confirmPassword: Optional[str] = None
    subscription_id: Optional[int] = 4
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    role: str
    company_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    company_phone_number: Optional[str] = None
    company_email: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None
