from schemas.user_subscription_schema import UserSubscriptionCreate
from core.database import get_database

async def create_user_subscription(subscription: UserSubscriptionCreate):
    conn = await get_database()
    try:
        await conn.execute(
            'INSERT INTO "usersubscription" (user_id, subscription_id, stripe_customer_id, stripe_subscription_id, status, start_date, end_date) VALUES ($1, $2, $3, $4, $5, $6, $7)',
            subscription.user_id, subscription.subscription_id, subscription.stripe_customer_id, subscription.stripe_subscription_id, subscription.status, subscription.start_date, subscription.end_date
        )
    finally:
        await conn.close()
