from core.database import get_database
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from schemas.company_schema import CompanyRead  # Assuming CompanyRead schema exists
from typing import Optional, List
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserCompanyService:
    async def create_user_company(
        self, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Associates a user with a company in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO usercompany (
                user_id, company_id
            ) VALUES (
                $1, $2
            )
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
            logging.error(f"Error creating user-company association: {e}")
            await conn.close()
            raise

    async def get_user_company(self, user_company_id: int) -> Optional[UserCompanyRead]:
        """
        Retrieves a user-company association by its ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, user_id, company_id
            FROM usercompany
            WHERE id = $1
        """
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
            logging.error(f"Error retrieving user-company association: {e}")
            await conn.close()
            raise

    async def update_user_company(
        self, user_company_id: int, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Updates an existing user-company association in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE usercompany
            SET user_id = $1, company_id = $2
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
            logging.error(f"Error updating user-company association: {e}")
            await conn.close()
            raise

    async def delete_user_company(self, user_company_id: int) -> bool:
        """
        Deletes a user-company association from the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM usercompany WHERE id = $1"
        try:
            result = await conn.execute(query, user_company_id)
            await conn.close()
            return result == "DELETE 1"
        except Exception as e:
            logging.error(f"Error deleting user-company association: {e}")
            await conn.close()
            raise

    async def list_user_companies(self) -> List[UserCompanyRead]:
        """
        Retrieves all user-company associations from the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, user_id, company_id
            FROM usercompany
        """
        try:
            results = await conn.fetch(query)
            await conn.close()
            user_companies = [
                UserCompanyRead(
                    id=row["id"],
                    user_id=row["user_id"],
                    company_id=row["company_id"],
                )
                for row in results
            ]
            return user_companies
        except Exception as e:
            logging.error(f"Error listing user-company associations: {e}")
            await conn.close()
            raise

    async def does_user_belong_to_company(self, user_id: int, company_id: int) -> bool:
        """
        Checks if a user belongs to a specific company.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT COUNT(*) FROM usercompany
            WHERE user_id = $1 AND company_id = $2
        """
        try:
            count = await conn.fetchval(query, user_id, company_id)
            await conn.close()
            return count > 0
        except Exception as e:
            logging.error(f"Error checking user-company membership: {e}")
            await conn.close()
            raise

    async def get_company_for_user(self, user_id: int) -> Optional[UserCompanyRead]:
        """
        Retrieves the company (or companies) a user belongs to.
        Returns a list of CompanyRead objects as a user can potentially belong to multiple companies.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
                    SELECT
                    company_id,user_id
                    FROM usercompany
                    WHERE user_id = $1
                            """
        try:
            result = await conn.fetchrow(query, user_id)
            await conn.close()
            if result:
                retcompany = UserCompanyRead(
                    id=result["id"],
                    user_id=result["user_id"],
                    company_id=result["company_id"],
                )
                return retcompany
            return None
        except Exception as e:
            logging.error(f"Error retrieving company for user: {e}")
            await conn.close()
            raise
