from core.database import get_database
from schemas.pdfqc_schema import PDFQCCreate, PDFQCRead
from typing import Optional, List
from datetime import datetime, timezone
import asyncpg
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PDFQCService:
    async def create_pdf_qc(self, data: PDFQCCreate) -> Optional[PDFQCRead]:
        conn = await get_database()
        query = """
            INSERT INTO pdfqc (
                doc_id, is_security, is_encrypted, has_bookmarks, has_tags,
                has_media, has_images, has_fonts, has_tables, has_links,
                has_annotations, has_form_fields, createdOn, updatedOn
            ) VALUES (
                $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14
            ) RETURNING *
        """
        now = datetime.now(timezone.utc)
        values = (
            data.doc_id,
            data.is_security,
            data.is_encrypted,
            data.has_bookmarks,
            data.has_tags,
            data.has_media,
            data.has_images,
            data.has_fonts,
            data.has_tables,
            data.has_links,
            data.has_annotations,
            data.has_form_fields,
            now,
            now,
        )
        result = await conn.fetchrow(query, *values)
        await conn.close()
        return PDFQCRead(**dict(result)) if result else None

    async def get_all_pdf_qc(self) -> List[PDFQCRead]:
        conn = await get_database()
        query = "SELECT qc.doc_id, file.filename,file.path as filepath,file.status,qc.is_security as has_metadata,qc.is_encrypted,qc.has_media,qc.has_bookmarks,qc.has_tags,qc.has_media,qc.has_images,qc.has_fonts,qc.has_tables,qc.has_links,qc.has_annotations,has_form_fields FROM public.pdffile as file inner join public.pdfqc as qc on  file.id=qc.doc_id"
        rows = await conn.fetch(query)
        await conn.close()
        return [PDFQCRead(**dict(row)) for row in rows]

    async def get_pdf_qc(self, qc_id: int) -> Optional[PDFQCRead]:
        conn = await get_database()
        query = """SELECT qc.doc_id, file.filename,file.path as filepath,file.status,qc.is_security as has_metadata,qc.is_encrypted,qc.has_media,qc.has_bookmarks,qc.has_tags,qc.has_media,qc.has_images,qc.has_fonts,qc.has_tables,qc.has_links,qc.has_annotations,has_form_fields FROM public.pdffile as file inner join public.pdfqc as qc on  file.id=qc.doc_id
                 where doc_id=$1"""
        row = await conn.fetchrow(query, qc_id)
        await conn.close()
        return PDFQCRead(**dict(row)) if row else None

    async def delete_pdf_qc(self, qc_id: int) -> Optional[PDFQCRead]:
        conn = await get_database()
        query = "DELETE FROM pdfqc WHERE id = $1 RETURNING *"
        row = await conn.fetchrow(query, qc_id)
        await conn.close()
        return PDFQCRead(**dict(row)) if row else None
