from pydantic import BaseModel


class UserCompanyCreate(BaseModel):
    user_id: int
    company_id: int


class UserCompanyRead(UserCompanyCreate):
    id: int

    class Config:
        from_attributes = True
