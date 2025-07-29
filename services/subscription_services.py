from core.database import get_database
from schemas.subscription_schema import (
    SubscriptionCreate,
    SubscriptionRead,
   )
from typing import List, Optional
import asyncpg
from datetime import datetime, timezone
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SubscriptionService:
    async def create_subscription(
        self, subscription_data: SubscriptionCreate
    ) -> Optional[SubscriptionRead]:
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO subscription (
                plan_name, plan_details, stripe_monthly_price_id, stripe_yearly_price_id,monthly_price,yearly_price,createdOn, updatedOn
            ) VALUES ($1, $2, $3, $4,$5, $6,$7,$8)
            RETURNING id, plan_name, plan_details, stripe_monthly_price_id, stripe_yearly_price_id,monthly_price,yearly_price, createdOn, updatedOn
        """
        values = (
            subscription_data.plan_name,
            subscription_data.plan_details,
            subscription_data.stripe_monthly_price_id,
            subscription_data.stripe_yearly_price_id,
            subscription_data.monthly_price,
            subscription_data.yearly_price,
            datetime.now(timezone.utc),
            None,
        )
        results = await conn.fetch(query, *values)
        fr: Optional[SubscriptionRead] = None
        if results:
            row = results[0]
            logger.info(row)
            fr = SubscriptionRead(
                id=row["id"],
                plan_name=row["plan_name"],
                plan_details=row["plan_details"],
                stripe_monthly_price_id=row["stripe_monthly_price_id"],
                stripe_yearly_price_id=row["stripe_yearly_price_id"],
                monthly_price=row["monthly_price"],
                yearly_price=row["yearly_price"],
                createdOn=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                updatedOn=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S") if row["updatedon"] else None,
            )

        await conn.close()
        return fr

    async def get_all_subscriptions(self) -> list[SubscriptionRead]:
        finalresult: list[SubscriptionRead] = []
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM subscription"
        results = await conn.fetch(query)
        await conn.close()
        if results:
            for row in results:
                fr = SubscriptionRead(
                    id=row["id"],
                    plan_name=row["plan_name"],
                    plan_details=row["plan_details"],
                    stripe_monthly_price_id=row["stripe_monthly_price_id"],
                    stripe_yearly_price_id=row["stripe_yearly_price_id"],
                    monthly_price=row["monthly_price"],
                    yearly_price=row["yearly_price"],
                    createdOn=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedOn=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S") if row["updatedon"] else None,
                )
                finalresult.append(fr)
        return finalresult

    async def get_subscription(
        self, subscription_id: int
    ) -> Optional[SubscriptionRead]:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM subscription WHERE id = $1"
        result = await conn.fetch(query, subscription_id)
        await conn.close()
        if result:
            row = result[0]
            fr = SubscriptionRead(
                id=row["id"],
                plan_name=row["plan_name"],
                plan_details=row["plan_details"],
                stripe_monthly_price_id=row["stripe_monthly_price_id"],
                stripe_yearly_price_id=row["stripe_yearly_price_id"],
                monthly_price=row["monthly_price"],
                yearly_price=row["yearly_price"],
                createdOn=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                updatedOn=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S") if row["updatedon"] else None,
            )
        return fr

    async def update_subscription(
        self, subscription_id: int, subscription_data: SubscriptionCreate
    ) -> Optional[SubscriptionRead]:
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE subscription SET
                plan_name = $1,
                plan_details = $2,
                stripe_monthly_price_id = $3,
                stripe_yearly_price_id = $4,
                monthly_price = $5,
                yearly_price = $6,
                updatedOn = $7
            WHERE id = $8
            RETURNING id, plan_name, plan_details, stripe_monthly_price_id, stripe_yearly_price_id, monthly_price, yearly_price, createdOn, updatedOn
        """
        values = (
            subscription_data.plan_name,
            subscription_data.plan_details,
            subscription_data.stripe_monthly_price_id,
            subscription_data.stripe_yearly_price_id,
            subscription_data.monthly_price,
            subscription_data.yearly_price,
            datetime.now(timezone.utc),
            subscription_id,
        )
        result = await conn.fetchrow(query, *values)
        await conn.close()
        return SubscriptionRead(**dict(result)) if result else None

    async def delete_subscription(
        self, subscription_id: int
    ) -> Optional[SubscriptionRead]:
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM subscription WHERE id = $1 RETURNING *"
        result = await conn.fetchrow(query, subscription_id)
        await conn.close()
        return SubscriptionRead(**dict(result)) if result else None
