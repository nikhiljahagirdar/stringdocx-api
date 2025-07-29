import asyncpg
from core.database import get_database
from typing import List, Optional
from schemas.user_schema import GetUser

class AdminService:
    async def get_all_users(self) -> List[GetUser]:
        conn: asyncpg.Connection = await get_database()
        query = '''
            SELECT id, email, phone_number, profile_picture, firstname, lastname, role, subscription_id,  createdon, updatedon
            FROM "user"
            ORDER BY createdon
        '''
        result = await conn.fetch(query)
        await conn.close()
        users: List[GetUser] = []
        for user in result:
            users.append(
                GetUser(
                    id=int(user["id"]),
                    email=user["email"],
                    phone_number=user.get("phone_number"),
                    profile_picture=user.get("profile_picture"),
                    firstname=user["firstname"],
                    lastname=user["lastname"],
                    subscription_id=user.get("subscription_id"),
                    role=user["role"],
                    createdOn=user["createdon"],
                    updatedOn=user["updatedon"],
                )
            )
        return users

    async def get_user(self, user_id: int) -> Optional[GetUser]:
        conn: asyncpg.Connection = await get_database()
        query = '''
            SELECT id, email, phone_number, profile_picture, firstname, lastname, subscription_id, company_id, role, createdon, updatedon
            FROM "user"
            WHERE id = $1
        '''
        row = await conn.fetchrow(query, user_id)
        await conn.close()
        if row:
            return GetUser(
                id=int(row["id"]),
                email=row["email"],
                phone_number=row.get("phone_number"),
                profile_picture=row.get("profile_picture"),
                firstname=row["firstname"],
                lastname=row["lastname"],
                subscription_id=row.get("subscription_id"),
                company_id=row.get("company_id"),
                role=row["role"],
                createdOn=row["createdon"],
                updatedOn=row["updatedon"],
            )
        return None
