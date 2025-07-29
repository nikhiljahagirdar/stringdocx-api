from fastapi import APIRouter, Depends, HTTPException
from schemas.user_subscription_schema import UserSubscriptionCreate
from schemas.user_payment_schema import UserPaymentCreate
from services.user_subscription_service import create_user_subscription
from services.user_payment_service import create_user_payment
import stripe
import os

router = APIRouter(prefix="/payment", tags=["payment"])

stripe.api_key = os.getenv("STRIPE_API_KEY")


@router.post("/create-checkout-session")
async def create_checkout_session(subscription: UserSubscriptionCreate):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": subscription.stripe_price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=os.getenv("FRONTEND_URL") + "/success",
            cancel_url=os.getenv("FRONTEND_URL") + "/cancel",
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stripe-webhook")
async def stripe_webhook(payload: dict):
    event = None
    try:
        event = stripe.Event.construct_from(payload, stripe.api_key)
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=str(e))

    # Handle the event
    if event.type == "checkout.session.completed":
        session = event.data.object
        # Create a new user subscription in your database
        # You'll need to extract the relevant information from the session object
        # and create a UserSubscriptionCreate object to pass to your service.
        pass
    elif event.type == "invoice.payment_succeeded":
        invoice = event.data.object
        # Create a new user payment in your database
        # You'll need to extract the relevant information from the invoice object
        # and create a UserPaymentCreate object to pass to your service.
        pass
    else:
        print("Unhandled event type {}".format(event.type))

    return {"status": "success"}
