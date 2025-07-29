from core.database import get_database
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from typing import Optional, List
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserCompanyService:
    async def create_user_company(
        self,
        user_company: UserCompanyCreate,
    ) -> Optional[UserCompanyRead]:
        """
        Creates a new user-company relationship entry in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO usercompany (
                user_id, company_id
            ) VALUES ($1, $2)
            RETURNING id, user_id, company_id
        """
        values = (
            user_company.user_id,
            user_company.company_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return UserCompanyRead(
                    id=result["id"],
                    user_id=result["user_id"],
                    company_id=result["company_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error creating user-company link: {e}")
            await conn.close()
            raise

    async def get_user_company(self, user_company_id: int) -> Optional[UserCompanyRead]:
        """
        Retrieves a user-company relationship by its ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM usercompany WHERE id = $1"
        try:
            result = await conn.fetchrow(query, user_company_id)
            await conn.close()
            if result:
                return UserCompanyRead(
                    id=result["id"],
                    user_id=result["user_id"],
                    company_id=result["company_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error getting user-company link: {e}")
            await conn.close()
            raise

    async def get_all_user_companies(self) -> List[UserCompanyRead]:
        """
        Retrieves all user-company relationship entries.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM usercompany"
        try:
            results = await conn.fetch(query)
            await conn.close()
            finalresult: List[UserCompanyRead] = []
            if results:
                for row in results:
                    fr = UserCompanyRead(
                        id=row["id"],
                        user_id=row["user_id"],
                        company_id=row["company_id"],
                    )
                    finalresult.append(fr)
            return finalresult
        except Exception as e:
            logging.error(f"Error getting all user-company links: {e}")
            await conn.close()
            raise

    async def update_user_company(
        self, user_company_id: int, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Updates a user-company relationship.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE usercompany SET
                user_id = $1,
                company_id = $2
            WHERE id = $3
            RETURNING id, user_id, company_id
        """
        values = (
            user_company.user_id,
            user_company.company_id,
            user_company_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return UserCompanyRead(
                    id=result["id"],
                    user_id=result["user_id"],
                    company_id=result["company_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error updating user-company link: {e}")
            await conn.close()
            raise

    async def delete_user_company(self, user_company_id: int) -> bool:
        """
        Deletes a user-company relationship by ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM usercompany WHERE id = $1 RETURNING *"
        try:
            result = await conn.fetchrow(query, user_company_id)
            await conn.close()
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting user-company link: {e}")
            await conn.close()
            raise
