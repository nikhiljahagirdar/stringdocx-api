from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_database
from schemas.master_config_schema import PdfMasterConfigCreate, PdfMasterConfigRead
from services.master_config_service import PdfMasterConfigService


router = APIRouter(prefix="/pdf-config", tags=["pdf-configs"])


def get_pdf_config_service(db=Depends(get_database)):
    return PdfMasterConfigService()


@router.post(
    "/", response_model=PdfMasterConfigRead, status_code=status.HTTP_201_CREATED
)
async def create_pdf_config(
    config_data: PdfMasterConfigCreate,
    service: PdfMasterConfigService = Depends(get_pdf_config_service),
):
    new_config = await service.create_pdf_master_config(config_data)
    if not new_config:
        raise HTTPException(status_code=400, detail="PDF config creation failed.")
    return new_config


@router.get("/", response_model=list[PdfMasterConfigRead])
async def get_all_pdf_configs(
    service: PdfMasterConfigService = Depends(get_pdf_config_service),
):
    return await service.get_all_pdf_master_configs()


@router.get("/{config_id}", response_model=PdfMasterConfigRead)
async def get_pdf_config(
    config_id: int,
    service: PdfMasterConfigService = Depends(get_pdf_config_service),
):
    config = await service.get_pdf_master_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="PDF config not found.")
    return config


@router.put("/{config_id}", response_model=PdfMasterConfigRead)
async def update_pdf_config(
    config_id: int,
    config_data: PdfMasterConfigCreate,
    service: PdfMasterConfigService = Depends(get_pdf_config_service),
):
    updated = await service.update_pdf_master_config(config_id, config_data)
    if not updated:
        raise HTTPException(status_code=404, detail="PDF config not found.")
    return updated


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pdf_config(
    config_id: int,
    service: PdfMasterConfigService = Depends(get_pdf_config_service),
):
    deleted = await service.delete_pdf_master_config(config_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="PDF config not found.")
    return None
