from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SubscriptionBase(BaseModel):
    plan_name: str
    plan_details: Optional[str] = None
    stripe_monthly_price_id: Optional[str] = None
    stripe_yearly_price_id: Optional[str] = None
    monthly_price: Optional[float] = None
    yearly_price: Optional[float] = None
    max_docs: int = 10


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    id: int
    createdOn: datetime
    updatedOn: Optional[datetime] = None

    class Config:
        orm_mode = True


class Subscription(SubscriptionBase):
    id: int
    createdOn: datetime
    updatedOn: Optional[datetime] = None

    class Config:
        orm_mode = True
