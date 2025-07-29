from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Depends,
    Form,
    HTTPException,
    BackgroundTasks,
)
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from pdfservices.qcCheck import analyze_pdf_quality
from core.database import get_database
from services.pdfFile_service import PDFFileService
from services.user_service import UserService
from services.pdfqc_service import PDFQCService
from services.status_service import StatusService
from schemas.pdffile_schema import PDFFileRead, PDFFileCreate
from schemas.pdfqc_schema import PDFQCRead, PDFQCCreate
from schemas.status_schema import SiteStatusRead, SiteStatusCreate
import logging
from fastapi.responses import FileResponse
from pdfservices.bookmarks import add_bookmarks_to_pdf_file

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


router = APIRouter(prefix="/pdf", tags=["pdf"])

MAX_FILE_SIZE = 90 * 1024 * 1024  # 5 MB

upload_dir = os.getenv("UPLOAD_DIR", "uploads")


def get_user_service(db=Depends(get_database)):
    return UserService()


def get_pdf_service(db=Depends(get_database)):
    return PDFFileService()


def get_pdfqc_service(db=Depends(get_database)):
    return PDFQCService()


def get_status_service(db=Depends(get_database)):
    return StatusService()


async def qc_background_task(
    files: [],
    pdfqcservice: PDFQCService = Depends(get_pdfqc_service),
    statusservice: StatusService = Depends(get_status_service),
):
    try:
        logger.info("Starting background task for PDF QC files are", files)
        for file in files:
            statuscreate: SiteStatusCreate = SiteStatusCreate(
                status_type="PDF_QC_START",
                status_message=f"PDF QC completed for {file.filename}.",
                pdf_file_id=file.id,
            )
            full_file_path = os.path.abspath(os.path.join(file.path, file.filename))

            qcresult = await analyze_pdf_quality(full_file_path)
            pdfqccreate: PDFQCCreate = PDFQCCreate(
                doc_id=file.id,
                is_security=qcresult["is_security"],
                is_encrypted=qcresult["is_encrypted"],
                has_bookmarks=qcresult["has_bookmarks"],
                has_tags=qcresult["has_tags"],
                has_annotations=qcresult["has_annotations"],
                has_form_fields=qcresult["has_form_fields"],
                has_images=qcresult["has_images"],
                has_fonts=qcresult["has_fonts"],
                has_tables=qcresult["has_tables"],
                has_links=qcresult["has_links"],
                has_media=qcresult["has_media"],
            )
            await pdfqcservice.create_pdf_qc(pdfqccreate)
            statuscreate: SiteStatusCreate = SiteStatusCreate(
                status_type="PDF_QC_END",
                status_message=f"PDF QC completed for {file.filename}.",
                pdf_file_id=file.id,
            )
            await statusservice.create_site_status(statuscreate)

    except Exception as e:
        logger.error(f"Error in background task: {e}")


async def add_bookmarks_to_pdf_files(source, destination):
    bookmarks = add_bookmarks_to_pdf_file(source, destination)


@router.post("/upload-pdf/")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    user_id: int = Form(...),
    files: list[UploadFile] = File(...),
    pdfservice: PDFQCService = Depends(get_pdf_service),
    pdfqcservice: PDFQCService = Depends(get_pdfqc_service),
    statusservice: StatusService = Depends(get_status_service),
    
):
    # Ensure uploads/user_id directory exists
    try:
        upload_dir = os.path.join("uploads", str(user_id))
        os.makedirs(upload_dir, exist_ok=True)
        relative_path = "uploads/" + str(user_id)
        results = []
        for file in files:
            if file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail=f"Only PDF files are allowed. Invalid file: {file.filename}",
                )

            contents = await file.read()
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds 5 MB limit: {file.filename}",
                )

            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as f_out:
                f_out.write(contents)
                pdffilecreate: PDFFileCreate = PDFFileCreate(
                    user_id=user_id,
                    filename=file.filename or "unnamed.pdf",
                    path=relative_path,
                    size=len(contents),
                    original_filename=file.filename,
                    status="uploaded",
                    status_message=f"File {file.filename} uploaded successfully.",
                )
                pdffile: PDFFileRead = await pdfservice.create_pdf_file(pdffilecreate)
                if pdffile:
                    results.append(pdffile)
                    statuscreate: SiteStatusCreate = SiteStatusCreate(
                        status_type="UPLOAD_FILE",
                        status_message=f"File {file.filename} uploaded successfully.",
                        pdf_file_id=pdffile.id,
                    )
                    await statusservice.create_site_status(statuscreate)


    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return results


@router.get("/getpds")
async def getdocs(pdfqcservice: PDFQCService = Depends(get_pdfqc_service)):
    try:
        return await pdfqcservice.get_all_pdf_qc()
    except Exception as e:
        logger.error(f"Error uploading file: {e}")


@router.get("/get_pdf/{id}")
async def get_pdf(id: int, pdf_file_service: PDFFileService = Depends(get_pdf_service)):
    try:
        pdf_file = await pdf_file_service.get_pdf_file(id)
        if not pdf_file:
            raise HTTPException(status_code=404, detail="PDF file not found")
        file_path = os.path.join(pdf_file.path, pdf_file.filename)
        logger.info(f"Serving file: {file_path}")
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            path=file_path, filename=pdf_file.filename, media_type="application/pdf"
        )
    except Exception as e:
        logger.error(f"Error fetching PDF: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
