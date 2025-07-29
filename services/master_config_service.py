from core.database import get_database
from schemas.master_config_schema import PdfMasterConfigCreate, PdfMasterConfigRead
from typing import Optional, List
from datetime import datetime, timezone
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PdfMasterConfigService:
    async def create_pdf_master_config(
        self, config: PdfMasterConfigCreate
    ) -> Optional[PdfMasterConfigRead]:
        """
        Creates a new PDF master config entry in the database.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO pdfMasterConfig (
                configType, configName, configValue, configDescription, isChild, createdOn, updatedOn
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, configType, configName, configValue, configDescription, isChild, createdOn, updatedOn
        """
        now = datetime.now(timezone.utc)
        values = (
            config.configType,
            config.configName,
            config.configValue,
            config.configDescription,
            config.isChild,
            now,
            now,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return PdfMasterConfigRead(
                    id=result["id"],
                    configType=result["configtype"],
                    configName=result["configname"],
                    configValue=result["configvalue"],
                    configDescription=result["configdescription"],
                    isChild=result["ischild"],
                    createdOn=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedOn=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S")
                    if result["updatedon"]
                    else None,
                )
            return None
        except Exception as e:
            logging.error(f"Error creating PDF master config: {e}")
            await conn.close()
            raise

    async def get_pdf_master_config(
        self, config_id: int
    ) -> Optional[PdfMasterConfigRead]:
        """
        Retrieves a PDF master config entry by its ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM pdfMasterConfig WHERE id = $1"
        try:
            result = await conn.fetchrow(query, config_id)
            await conn.close()
            if result:
                return PdfMasterConfigRead(
                    id=result["id"],
                    configType=result["configtype"],
                    configName=result["configname"],
                    configValue=result["configvalue"],
                    configDescription=result["configdescription"],
                    isChild=result["ischild"],
                    createdOn=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedOn=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S")
                    if result["updatedon"]
                    else None,
                )
            return None
        except Exception as e:
            logging.error(f"Error getting PDF master config: {e}")
            await conn.close()
            raise

    async def get_all_pdf_master_configs(self) -> List[PdfMasterConfigRead]:
        """
        Retrieves all PDF master config entries.
        """
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM pdfMasterConfig"
        try:
            results = await conn.fetch(query)
            await conn.close()
            finalresult: List[PdfMasterConfigRead] = []
            for row in results:
                fr = PdfMasterConfigRead(
                    id=row["id"],
                    configType=row["configtype"],
                    configName=row["configname"],
                    configValue=row["configvalue"],
                    configDescription=row["configdescription"],
                    isChild=row["ischild"],
                    createdOn=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedOn=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S")
                    if row["updatedon"]
                    else None,
                )
                finalresult.append(fr)
            return finalresult
        except Exception as e:
            logging.error(f"Error getting all PDF master configs: {e}")
            await conn.close()
            raise

    async def update_pdf_master_config(
        self, config_id: int, config: PdfMasterConfigCreate
    ) -> Optional[PdfMasterConfigRead]:
        """
        Updates an existing PDF master config entry.
        """
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE pdfMasterConfig SET
                configType = $1,
                configName = $2,
                configValue = $3,
                configDescription = $4,
                isChild = $5,
                updatedOn = $6
            WHERE id = $7
            RETURNING id, configType, configName, configValue, configDescription, isChild, createdOn, updatedOn
        """
        values = (
            config.configType,
            config.configName,
            config.configValue,
            config.configDescription,
            config.isChild,
            datetime.now(timezone.utc),
            config_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return PdfMasterConfigRead(
                    id=result["id"],
                    configType=result["configtype"],
                    configName=result["configname"],
                    configValue=result["configvalue"],
                    configDescription=result["configdescription"],
                    isChild=result["ischild"],
                    createdOn=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updatedOn=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S")
                    if result["updatedon"]
                    else None,
                )
            return None
        except Exception as e:
            logging.error(f"Error updating PDF master config: {e}")
            await conn.close()
            raise

    async def delete_pdf_master_config(self, config_id: int) -> bool:
        """
        Deletes a PDF master config entry by its ID.
        """
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM pdfMasterConfig WHERE id = $1 RETURNING *"
        try:
            result = await conn.fetchrow(query, config_id)
            await conn.close()
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting PDF master config: {e}")
            await conn.close()
            raise
