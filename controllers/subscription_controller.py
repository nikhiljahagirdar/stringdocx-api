from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from services.subscription_services import SubscriptionService
from schemas.subscription_schema import SubscriptionCreate, SubscriptionRead

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
subscription_service = SubscriptionService()


@router.get("/", response_model=List[SubscriptionRead])
async def get_all_subscriptions():
    subscriptions = await subscription_service.get_all_subscriptions()
    return subscriptions


@router.get("/{subscription_id}", response_model=SubscriptionRead)
async def get_subscription_by_id(subscription_id: int):
    subscription = await subscription_service.get_subscription(subscription_id)
    if subscription:
        return subscription
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
    )


@router.post("/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(subscription_data: SubscriptionCreate):
    try:
        subscription = await subscription_service.create_subscription(subscription_data)
        return subscription
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{subscription_id}", response_model=SubscriptionRead)
async def update_subscription(
    subscription_id: int, subscription_data: SubscriptionCreate
):
    try:
        subscription = await subscription_service.update_subscription(
            subscription_id, subscription_data
        )
        if subscription:
            return subscription
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(subscription_id: int):
    deleted_subscription = await subscription_service.delete_subscription(
        subscription_id
    )
    if not deleted_subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return {"message": "Subscription deleted successfully"}
