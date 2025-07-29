from core.database import get_database
from schemas.pdffile_schema import PDFFileCreate, PDFFileRead
from typing import Optional, List
from datetime import datetime, timezone
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PDFFileService:
    async def create_pdf_file(self, data: PDFFileCreate) -> Optional[PDFFileRead]:
        conn = await get_database()
        query = """
            INSERT INTO pdffile (
                user_id, filename, path, size, original_filename, processed_filename,
                processed_path, processing_start_time, processing_end_time, status,status_message,
                createdOn, updatedOn
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
            RETURNING *
        """
        now = datetime.now(timezone.utc)
        values = (
            data.user_id,
            data.filename,
            data.path,
            data.size,
            data.original_filename,
            data.processed_filename,
            data.processed_path,
            data.processing_start_time,
            data.processing_end_time,
            data.status,
            data.status_message,
            now,
            now,
        )
        result = await conn.fetchrow(query, *values)
        await conn.close()
        return PDFFileRead(**dict(result)) if result else None

    async def get_all_pdf_files(self) -> List[PDFFileRead]:
        conn = await get_database()
        query = "SELECT * FROM pdffile"
        rows = await conn.fetch(query)
        await conn.close()
        return [PDFFileRead(**dict(row)) for row in rows]

    async def get_pdf_file(self, file_id: int) -> Optional[PDFFileRead]:
        conn = await get_database()
        query = "SELECT * FROM pdffile WHERE id = $1"
        row = await conn.fetchrow(query, file_id)
        await conn.close()
        return PDFFileRead(**dict(row)) if row else None

    async def delete_pdf_file(self, file_id: int) -> Optional[PDFFileRead]:
        conn = await get_database()
        query = "DELETE FROM pdffile WHERE id = $1 RETURNING *"
        row = await conn.fetchrow(query, file_id)
        await conn.close()
        return PDFFileRead(**dict(row)) if row else None

    async def update_pdf_file_status(self, file_id: int, status: str):
        conn = await get_database()
        query = "UPDATE public.pdffile set status=$1 where id=$2 RETURNING *"
        values = (status, file_id)
        await conn.execute(query, *values)
        row = await conn.fetchrow(query, file_id)
        await conn.close()
        
        
