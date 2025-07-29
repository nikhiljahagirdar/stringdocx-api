from schemas.user_payment_schema import UserPaymentCreate
from core.database import get_database

async def create_user_payment(payment: UserPaymentCreate):
    conn = await get_database()
    try:
        await conn.execute(
            'INSERT INTO "userpayment" (user_subscription_id, stripe_payment_id, amount, currency, status, payment_date) VALUES ($1, $2, $3, $4, $5, $6)',
            payment.user_subscription_id, payment.stripe_payment_id, payment.amount, payment.currency, payment.status, payment.payment_date
        )
    finally:
        await conn.close()
