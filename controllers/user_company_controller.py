from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from core import security
from services.user_comapny_service import UserCompanyService
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from schemas.auth_schema import GoogleAuth, Login, Register
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_user_company_service():
    return UserCompanyService()

router = APIRouter(prefix="/user-company", tags=["User Companies"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_company(
    user_company_data: UserCompanyCreate,
    service: UserCompanyService = Depends(get_user_company_service)
    ):
    user_company = UserCompanyCreate(user_id=user_company_data.user_id, company_id=user_company_data.company_id)
    new_user_company = await service.create_user_company(user_company)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_user_company.model_dump(),
    )


@router.get("/{user_company_id}")
async def get_user_company(
    user_company_id: int,
    service: UserCompanyService = Depends(get_user_company_service),
):
    user_company = await service.get_user_company(user_company_id)
    if not user_company:
        raise HTTPException(status_code=404, detail="User-Company association not found.")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_company.model_dump(),
    )


@router.get("/")
async def get_all_user_companies(
    service: UserCompanyService = Depends(get_user_company_service),
):
    user_companies = await service.list_user_companies()
    return JSONResponse(
        content=[uc.model_dump() for uc in user_companies],
    )


@router.put("/", )
async def update_user_company(
    user_company_id: int,
    user_company_data: UserCompanyCreate,
    service: UserCompanyService = Depends(get_user_company_service),
):
    updated_user_company = await service.update_user_company(user_company_id, user_company_data)
    if not updated_user_company:
        raise HTTPException(status_code=404, detail="User-Company association not found.")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_user_company.model_dump(),
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_company(
    user_company_id: int,
    service: UserCompanyService = Depends(get_user_company_service),
):
    deleted = await service.delete_user_company(user_company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User-Company association not found.")
    return None
