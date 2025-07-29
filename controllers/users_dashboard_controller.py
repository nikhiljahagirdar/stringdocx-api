from fastapi import APIRouter, Depends
from services.users_dashboard_service import UsersDashboardService

router = APIRouter(prefix="/users-dashboard", tags=["Users-Dashboard"])

def get_users_dashboard_service():
    return UsersDashboardService()

@router.get("/user-count")
async def get_user_count(
    users_dashboard_service: UsersDashboardService = Depends(get_users_dashboard_service),
):
    return await users_dashboard_service.get_user_count()

@router.get("/document-count")
async def get_document_count(
    users_dashboard_service: UsersDashboardService = Depends(get_users_dashboard_service),
):
    return await users_dashboard_service.get_document_count()

@router.get("/total-revenue")
async def get_total_revenue(
    users_dashboard_service: UsersDashboardService = Depends(get_users_dashboard_service),
):
    return await users_dashboard_service.get_total_revenue()

@router.get("/subscription-count")
async def get_subscription_count(
    users_dashboard_service: UsersDashboardService = Depends(get_users_dashboard_service),
):
    return await users_dashboard_service.get_subscription_count()
