from pydantic import BaseModel
from datetime import datetime

class UserPaymentBase(BaseModel):
    user_subscription_id: int
    stripe_payment_id: str
    amount: float
    currency: str
    status: str
    payment_date: datetime

class UserPaymentCreate(UserPaymentBase):
    pass

class UserPayment(UserPaymentBase):
    id: int
    createdOn: datetime
    updatedOn: datetime | None = None

    class Config:
        orm_mode = True
