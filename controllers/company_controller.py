from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List 
from services.company_service import CompanyService
from schemas.company_schema import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["Companies"])

def get_company_service():
    return CompanyService()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
):
    new_company = await service.create_company(company_data)
    if not new_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company creation failed.")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_company.model_dump(),
    )


@router.get("/")
async def get_all_companies(
    service: CompanyService = Depends(get_company_service),
):
    companies = await service.list_companies()
    return JSONResponse(content=[c.model_dump() for c in companies])


@router.get("/{company_id}")
async def get_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service),
):
    company = await service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
    return JSONResponse(content=company.model_dump())


@router.put("/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: int,
    company_data: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
):
    updated = await service.update_company(company_id, company_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated.model_dump())


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_company_service),
):
    deleted = await service.delete_company(company_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
    return None
