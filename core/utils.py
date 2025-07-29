from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
from fastapi import HTTPException, status

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


async def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        if "email" not in idinfo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google ID token",
            )
        return idinfo["email"]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google ID token"
        )
