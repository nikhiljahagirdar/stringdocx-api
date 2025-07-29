from core.security import hash_password
import logging
from core.database import get_database
from datetime import datetime, timezone
import asyncpg
from typing import List, Optional
from schemas.user_schema import GetUser, CreateUser, GetUserPassword

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserService:
    async def get_all_users(self) -> List[GetUser]:
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, email, phone_number, profile_picture, firstname, lastname, role, subscription_id,  createdon, updatedon
            FROM "user"
            ORDER BY createdon
        """
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

    async def create_user(self, user_create_data: CreateUser) -> Optional[GetUser]:
        conn: asyncpg.Connection = await get_database()
        created_time = datetime.now(timezone.utc)
        query = """
            INSERT INTO "user" (
                email, password_hash, firstname, lastname, phone_number, profile_picture,
                subscription_id,  role, createdon, updatedon
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING *
        """
        values = (
            user_create_data.email,
            user_create_data.password,
            user_create_data.firstname,
            user_create_data.lastname,
            user_create_data.phone_number,
            user_create_data.profile_picture,
            user_create_data.subscription_id,
            user_create_data.role,
            created_time,
            created_time,
        )
        row = await conn.fetchrow(query, *values)
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

    async def get_user_by_email(self, email: str) -> Optional[GetUserPassword]:
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT 
  u.id, 
  u.email, 
  u.password_hash, 
  u.phone_number, 
  u.profile_picture, 
  u.firstname, 
  u.lastname, 
  u.role, 
  u.subscription_id, 
  uc.company_id, 
  u.createdon, 
  u.updatedon
FROM 
  "user" u
LEFT JOIN 
  usercompany uc 
ON 
  u.id = uc.user_id;
            WHERE email = $1
        """
        row = await conn.fetchrow(query, email)
        await conn.close()
        if row:
            return GetUserPassword(
                id=int(row["id"]),
                email=row["email"],
                phone_number=row.get("phone_number"),
                profile_picture=row.get("profile_picture"),
                firstname=row["firstname"],
                lastname=row["lastname"],
                password_hash=row["password_hash"],
                subscription_id=row.get("subscription_id"),
                role=row["role"],
                createdOn=row["createdon"],
                updatedOn=row["updatedon"],
            )
        return None

    async def get_user(self, user_id: int) -> Optional[GetUser]:
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, email, phone_number, profile_picture, firstname, lastname, subscription_id, company_id, role, createdon, updatedon
            FROM "user"
            WHERE id = $1
        """
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

    async def update_user(
        self, user_id: int, user_update_data: CreateUser
    ) -> Optional[GetUser]:
        conn: asyncpg.Connection = await get_database()
        password_hash = hash_password(user_update_data.password)
        updated_time = datetime.now(timezone.utc)
        query = """
            UPDATE "user"
            SET email = $1,
                password_hash = $2,
                firstname = $3,
                lastname = $4,
                phone_number = $5,
                profile_picture = $6,
                subscription_id = $7,
                company_id = $8,
                role = $9,
                updatedon = $10
            WHERE id = $11
            RETURNING *
        """
        values = (
            user_update_data.email,
            password_hash,
            user_update_data.firstname,
            user_update_data.lastname,
            user_update_data.phone_number,
            user_update_data.profile_picture,
            user_update_data.subscription_id,
            user_update_data.company_id,
            user_update_data.role,
            updated_time,
            user_id,
        )
        row = await conn.fetchrow(query, *values)
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

    async def delete_user(self, user_id: int):
        conn: asyncpg.Connection = await get_database()
        query = 'DELETE FROM "user" WHERE id = $1'
        await conn.execute(query, user_id)
        await conn.close()

    async def update_user_doc_count(self, user_id: int, new_doc_count: int):
        conn: asyncpg.Connection = await get_database()
        updated_time = datetime.now(timezone.utc)
        query = """
            UPDATE "user"
            SET doc_count = $1,
                updatedon = $2
            WHERE id = $3
        """
        await conn.execute(query, new_doc_count, updated_time, user_id)
        await conn.close()
