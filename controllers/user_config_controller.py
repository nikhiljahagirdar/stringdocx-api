from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_database
from schemas.user_config_schema import PdfUserConfigCreate, PdfUserConfigRead
from services.user_config_service import PdfUserConfigService

router = APIRouter(prefix="/user-config", tags=["user-configs"])

def get_user_config_service(db=Depends(get_database)):
    return PdfUserConfigService()


@router.post("/", response_model=PdfUserConfigRead, status_code=status.HTTP_201_CREATED)
async def create_user_config(
    config_data: PdfUserConfigCreate,
    service: PdfUserConfigService = Depends(get_user_config_service),
):
    new_config = await service.create_pdf_user_config(config_data)
    if not new_config:
        raise HTTPException(status_code=400, detail="User config creation failed.")
    return new_config


@router.get("/", response_model=list[PdfUserConfigRead])
async def get_all_user_configs(
    service: PdfUserConfigService = Depends(get_user_config_service),
):
    return await service.get_all_pdf_user_configs()


@router.get("/{config_id}", response_model=PdfUserConfigRead)
async def get_user_config(
    config_id: int,
    service: PdfUserConfigService = Depends(get_user_config_service),
):
    config = await service.get_pdf_user_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="User config not found.")
    return config


@router.put("/{config_id}", response_model=PdfUserConfigRead)
async def update_user_config(
    config_id: int,
    config_data: PdfUserConfigCreate,
    service: PdfUserConfigService = Depends(get_user_config_service),
):
    updated = await service.update_pdf_user_config(config_id, config_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User config not found.")
    return updated


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_config(
    config_id: int,
    service: PdfUserConfigService = Depends(get_user_config_service),
):
    deleted = await service.delete_pdf_user_config(config_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User config not found.")
    return None
