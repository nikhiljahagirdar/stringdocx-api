from core.database import get_database
from schemas.status_schema import SiteStatusCreate, SiteStatusRead
from typing import Optional, List
from datetime import datetime, timezone
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StatusService:
    async def create_site_status(
        self,
        site_status: SiteStatusCreate,
    ) -> Optional[SiteStatusRead]:
        """
        Creates a new site status entry in the database.

        Args:
            site_status: The SiteStatusCreate object containing the data for the new entry.

        Returns:
            The created site status entry as a SiteStatusRead object.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO sitestatus (
                status_type, status_message, pdf_file_id, createdon, updatedon
            ) VALUES ($1, $2, $3, $4, $5)
            RETURNING id, status_type, status_message, pdf_file_id, createdon, updatedon
        """
        values = (
            site_status.status_type,
            site_status.status_message,
            site_status.pdf_file_id,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return SiteStatusRead(
                    id=result["id"],
                    status_type=result["status_type"],
                    status_message=result["status_message"],
                    pdf_file_id=result["pdf_file_id"],
                    createdon=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedon=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error creating site status: {e}")
            await conn.close()
            raise

    async def get_site_status(self, site_status_id: int) -> Optional[SiteStatusRead]:
        """
        Retrieves a site status entry by its ID.

        Args:
            site_status_id: The ID of the site status entry to retrieve.

        Returns:
            The site status entry as a SiteStatusRead object if found, otherwise None.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM sitestatus WHERE id = $1"
        try:
            result = await conn.fetchrow(query, site_status_id)
            await conn.close()
            if result:
                return SiteStatusRead(
                    id=result["id"],
                    status_type=result["status_type"],
                    status_message=result["status_message"],
                    pdf_file_id=result["pdf_file_id"],
                    createdon=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedon=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error getting site status: {e}")
            await conn.close()
            raise

    async def get_all_site_statuses(self) -> List[SiteStatusRead]:
        """
        Retrieves all site status entries.
        Returns:
            A list of site status entries as SiteStatusRead objects.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM sitestatus"
        try:
            results = await conn.fetch(query)
            await conn.close()
            finalresult: List[SiteStatusRead] = []
            if results:
                for row in results:
                    fr = SiteStatusRead(
                        id=row["id"],
                        status_type=row["status_type"],
                        status_message=row["status_message"],
                        pdf_file_id=row["pdf_file_id"],
                        createdon=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                        updatedon=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    finalresult.append(fr)
            return finalresult
        except Exception as e:
            logging.error(f"Error getting all site statuses: {e}")
            await conn.close()
            raise

    async def update_site_status(
        self, site_status_id: int, site_status: SiteStatusCreate
    ) -> Optional[SiteStatusRead]:
        """
        Updates an existing site status entry.

        Args:
            site_status_id: The ID of the site status entry to update.
            site_status: The SiteStatusCreate object containing the updated data.

        Returns:
            The updated site status entry as a SiteStatusRead object if updated, otherwise None.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE sitestatus SET
                status_type = $1,
                status_message = $2,
                pdf_file_id = $3,
                updatedon = $4
            WHERE id = $5
            RETURNING id, status_type, status_message, pdf_file_id, createdon, updatedon
        """
        values = (
            site_status.status_type,
            site_status.status_message,
            site_status.pdf_file_id,
            datetime.now(timezone.utc),
            site_status_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return SiteStatusRead(
                    id=result["id"],
                    status_type=result["status_type"],
                    status_message=result["status_message"],
                    pdf_file_id=result["pdf_file_id"],
                    createdon=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedon=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error updating site status: {e}")
            await conn.close()
            raise

    async def delete_site_status(self, site_status_id: int) -> bool:
        """
        Deletes a site status entry by its ID.

        Args:
            site_status_id: The ID of the site status entry to delete.

        Returns:
            True if the entry was deleted, False otherwise.
        """
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM sitestatus WHERE id = $1 RETURNING *"
        try:
            result = await conn.fetchrow(query, site_status_id)
            await conn.close()
            return result is not None  # Returns True if a row was deleted
        except Exception as e:
            logging.error(f"Error deleting site status: {e}")
            await conn.close()
            raise
