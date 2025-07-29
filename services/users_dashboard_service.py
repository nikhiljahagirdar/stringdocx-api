import asyncpg
from core.database import get_database

class UsersDashboardService:
    async def get_user_count(self) -> dict:
        conn: asyncpg.Connection = await get_database()
        query = 'SELECT COUNT(*) FROM "user"'
        count = await conn.fetchval(query)
        await conn.close()
        return {"user_count": count}

    async def get_document_count(self) -> dict:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT COUNT(*) FROM pdf_file"
        count = await conn.fetchval(query)
        await conn.close()
        return {"document_count": count}

    async def get_total_revenue(self) -> dict:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT SUM(amount) FROM user_payment"
        revenue = await conn.fetchval(query)
        await conn.close()
        return {"total_revenue": revenue}

    async def get_subscription_count(self) -> dict:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT COUNT(*) FROM subscription"
        count = await conn.fetchval(query)
        await conn.close()
        return {"subscription_count": count}
