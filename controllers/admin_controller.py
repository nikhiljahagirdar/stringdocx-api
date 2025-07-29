from fastapi import APIRouter, Depends, HTTPException, status
from services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_admin_service():
    return AdminService()

@router.get("/users")
async def get_all_users(admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.get_all_users()

@router.get("/users/{user_id}")
async def get_user(user_id: int, admin_service: AdminService = Depends(get_admin_service)):
    user = await admin_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
