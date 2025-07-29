from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_database
from schemas.user_schema import GetUser, CreateUser
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

USER_NOT_FOUND = "User not found"

def get_user_service(db=Depends(get_database)):
    return UserService()

@router.get("/", response_model=list[GetUser])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()

@router.post("/", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUser, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(user_data)
    return user

@router.get("/{user_id}", response_model=GetUser)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    return user

@router.put("/{user_id}", response_model=GetUser)
async def update_user(
    user_id: int,
    user_data: CreateUser,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    await user_service.delete_user(user_id)
    return None
