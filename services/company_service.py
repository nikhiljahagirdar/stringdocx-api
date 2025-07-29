from core.database import get_database
from schemas.company_schema import CompanyCreate, CompanyRead
from typing import Optional, List
from datetime import datetime, timezone
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CompanyService:
    async def create_company(self, company: CompanyCreate) -> Optional[CompanyRead]:
        """
        Creates a new company entry in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO company (
                name, address, city, state, zip_code, country,
                phone_number, email, company_website, logo, subscription_id
            ) VALUES (
                $1, $2, $3, $4, $5, $6,
                $7, $8, $9, $10, $11
            )
            RETURNING id, name, address, city, state, zip_code, country,
                      phone_number, email, company_website, logo, subscription_id
        """

        values = (
            company.name,
            company.address,
            company.city,
            company.state,
            company.zip_code,
            company.country,
            company.phone_number,
            company.email,
            company.company_website,
            company.logo,
            company.subscription_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return CompanyRead(
                    id=result["id"],
                    name=result["name"],
                    address=result["address"],
                    city=result["city"],
                    state=result["state"],
                    zip_code=result["zip_code"],
                    country=result["country"],
                    phone_number=result["phone_number"],
                    email=result["email"],
                    company_website=result["company_website"],
                    logo=result["logo"],
                    subscription_id=result["subscription_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error creating company: {e}")
            await conn.close()
            raise

    async def get_company(self, company_id: int) -> Optional[CompanyRead]:
        """
        Retrieves a company entry by its ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, name, address, city, state, zip_code, country,
                   phone_number, email, company_website, logo, subscription_id
            FROM company
            WHERE id = $1
        """
        try:
            result = await conn.fetchrow(query, company_id)
            await conn.close()
            if result:
                return CompanyRead(
                    id=result["id"],
                    name=result["name"],
                    address=result["address"],
                    city=result["city"],
                    state=result["state"],
                    zip_code=result["zip_code"],
                    country=result["country"],
                    phone_number=result["phone_number"],
                    email=result["email"],
                    company_website=result["company_website"],
                    logo=result["logo"],
                    subscription_id=result["subscription_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error retrieving company: {e}")
            await conn.close()
            raise


     

    async def update_company(self, company_id: int, company: CompanyCreate) -> Optional[CompanyRead]:
        """
        Updates an existing company entry in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE company
            SET name = $1, address = $2, city = $3, state = $4, zip_code = $5, country = $6,
                phone_number = $7, email = $8, company_website = $9, logo = $10, subscription_id = $11
            WHERE id = $12
            RETURNING id, name, address, city, state, zip_code, country,
                      phone_number, email, company_website, logo, subscription_id
        """
        values = (
            company.name,
            company.address,
            company.city,
            company.state,
            company.zip_code,
            company.country,
            company.phone_number,
            company.email,
            company.company_website,
            company.logo,
            company.subscription_id,
            company_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return CompanyRead(
                    id=result["id"],
                    name=result["name"],
                    address=result["address"],
                    city=result["city"],
                    state=result["state"],
                    zip_code=result["zip_code"],
                    country=result["country"],
                    phone_number=result["phone_number"],
                    email=result["email"],
                    company_website=result["company_website"],
                    logo=result["logo"],
                    subscription_id=result["subscription_id"],
                )
            return None
        except Exception as e:
            logging.error(f"Error updating company: {e}")
            await conn.close()
            raise

    async def delete_company(self, company_id: int) -> bool:
        """
        Deletes a company entry from the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM company WHERE id = $1"
        try:
            result = await conn.execute(query, company_id)
            await conn.close()
            return result == "DELETE 1"
        except Exception as e:
            logging.error(f"Error deleting company: {e}")
            await conn.close()
            raise

    async def list_companies(self) -> List[CompanyRead]:
        """
        Retrieves all company entries from the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            SELECT id, name, address, city, state, zip_code, country,
                   phone_number, email, company_website, logo, subscription_id
            FROM company
        """
        try:
            results = await conn.fetch(query)
            await conn.close()
            companies = [
                CompanyRead(
                    id=row["id"],
                    name=row["name"],
                    address=row["address"],
                    city=row["city"],
                    state=row["state"],
                    zip_code=row["zip_code"],
                    country=row["country"],
                    phone_number=row["phone_number"],
                    email=row["email"],
                    company_website=row["company_website"],
                    logo=row["logo"],
                    subscription_id=row["subscription_id"],
                )
                for row in results
            ]
            return companies
        except Exception as e:
            logging.error(f"Error listing companies: {e}")
            await conn.close()
            raise
        
            
