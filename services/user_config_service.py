from core.database import get_database
import asyncpg
import logging
from typing import Optional, List
from datetime import datetime, timezone
from schemas.user_config_schema import PdfUserConfigCreate, PdfUserConfigRead


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PdfUserConfigService:
    async def create_pdf_user_config(
        self, config: PdfUserConfigCreate
    ) -> Optional[PdfUserConfigRead]:
        conn: asyncpg.Connection = await get_database()
        query = """
            INSERT INTO pdfUserConfig (
                config_id, user_id, doc_id, createdOn, updatedOn
            ) VALUES ($1, $2, $3, $4, $5)
            RETURNING id, config_id, user_id, doc_id, createdOn, updatedOn
        """
        values = (
            config.config_id,
            config.user_id,
            config.doc_id,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return PdfUserConfigRead(
                    id=result["id"],
                    config_id=result["config_id"],
                    user_id=result["user_id"],
                    doc_id=result["doc_id"],
                    created_on=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updated_on=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error creating PDF user config: {e}")
            await conn.close()
            raise

    async def get_pdf_user_config(self, config_id: int) -> Optional[PdfUserConfigRead]:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM pdfUserConfig WHERE id = $1"
        try:
            result = await conn.fetchrow(query, config_id)
            await conn.close()
            if result:
                return PdfUserConfigRead(
                    id=result["id"],
                    config_id=result["config_id"],
                    user_id=result["user_id"],
                    doc_id=result["doc_id"],
                    created_on=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updated_on=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error retrieving PDF user config: {e}")
            await conn.close()
            raise

    async def get_all_pdf_user_configs(self) -> List[PdfUserConfigRead]:
        conn: asyncpg.Connection = await get_database()
        query = "SELECT * FROM pdfUserConfig"
        try:
            results = await conn.fetch(query)
            await conn.close()
            configs = []
            for row in results:
                configs.append(
                    PdfUserConfigRead(
                        id=row["id"],
                        config_id=row["config_id"],
                        user_id=row["user_id"],
                        doc_id=row["doc_id"],
                        created_on=row["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                        updated_on=row["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )
            return configs
        except Exception as e:
            logging.error(f"Error fetching all PDF user configs: {e}")
            await conn.close()
            raise

    async def update_pdf_user_config(
        self, config_id: int, config: PdfUserConfigCreate
    ) -> Optional[PdfUserConfigRead]:
        conn: asyncpg.Connection = await get_database()
        query = """
            UPDATE pdfUserConfig SET
                config_id = $1,
                user_id = $2,
                doc_id = $3,
                updatedOn = $4
            WHERE id = $5
            RETURNING id, config_id, user_id, doc_id, createdOn, updatedOn
        """
        values = (
            config.config_id,
            config.user_id,
            config.doc_id,
            datetime.now(timezone.utc),
            config_id,
        )
        try:
            result = await conn.fetchrow(query, *values)
            await conn.close()
            if result:
                return PdfUserConfigRead(
                    id=result["id"],
                    config_id=result["config_id"],
                    user_id=result["user_id"],
                    doc_id=result["doc_id"],
                    created_on=result["createdon"].strftime("%Y-%m-%d %H:%M:%S"),
                    updated_on=result["updatedon"].strftime("%Y-%m-%d %H:%M:%S"),
                )
            return None
        except Exception as e:
            logging.error(f"Error updating PDF user config: {e}")
            await conn.close()
            raise

    async def delete_pdf_user_config(self, config_id: int) -> bool:
        conn: asyncpg.Connection = await get_database()
        query = "DELETE FROM pdfUserConfig WHERE id = $1 RETURNING id"
        try:
            result = await conn.fetchrow(query, config_id)
            await conn.close()
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting PDF user config: {e}")
            await conn.close()
            raise
