from pydantic import BaseModel
from datetime import datetime

class UserSubscriptionBase(BaseModel):
    user_id: int
    subscription_id: int
    stripe_customer_id: str
    stripe_subscription_id: str
    status: str
    start_date: datetime
    end_date: datetime | None = None

class UserSubscriptionCreate(UserSubscriptionBase):
    pass

class UserSubscription(UserSubscriptionBase):
    id: int
    createdOn: datetime
    updatedOn: datetime | None = None

    class Config:
        orm_mode = True
