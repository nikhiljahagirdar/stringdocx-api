from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from core import security
from services.user_service import UserService
from services.company_service import CompanyService
from services.user_comapny_service import UserCompanyService
from schemas.user_schema import GetUser, CreateUser
from schemas.company_schema import CompanyCreate
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from schemas.auth_schema import GoogleAuth, Login, Register
from typing import Optional
from core.security import hash_password, verify_password


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Dependency to inject UserService
def get_user_service():
    return UserService()


def get_company_service():
    return CompanyService()


def get_user_company_service():
    return UserCompanyService()


@router.post("/register", response_model=Register)
async def register_user(
    user_data: Register,
    user_service: UserService = Depends(get_user_service),
    company_service: CompanyService = Depends(get_company_service),
    user_company: UserCompanyService = Depends(get_user_company_service),
) -> JSONResponse:
    logger.info(f"Registering user with data: {user_data}")
    existing_user = await user_service.get_user_by_email(user_data.email)
    logger.info(f"Existing user: {existing_user}")
    company_id = None
    user = None
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if user_data.account_type == "company":
        try:
            company_id = 0
            company_data = CompanyCreate(
                name=user_data.company_name,
                address=user_data.address,
                city=user_data.city,
                state=user_data.state,
                zip_code=user_data.zip_code,
                phone_number=user_data.company_phone_number,
                email=user_data.company_email,
                company_website=user_data.website,
                subscription_id=user_data.subscription_id,
                logo=user_data.logo,
            )
            company = await company_service.create_company(company_data)
            if company is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create company: company object is None",
                )
            company_id = company.id
            if company_id is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create company: company ID is None after creation",
                )
            logger.info(f"company ID: {company_id}")
            hashed_password = hash_password(user_data.password)

            add_user = CreateUser(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                password=hashed_password,
                phone_number=user_data.phone_number,
                company_id=company_id,
                role=user_data.role,
            )
            user = await user_service.create_user(add_user)
            logger.info(f"User created with ID: {user.id}")  # type: ignore
            if user is not None:  # Add this check
                
                logger.info("Company registration attempt finished.")
            else:
                logger.warning(
                    "company_id is None, skipping UserCompanyCreate."
                )  # Log a warning
        except Exception as e:
            logger.error(f"Error during company registration: {e}")
            raise
    else:
        hashed_password = security.hash_password(user_data.password)
        add_user = CreateUser(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            password=hashed_password,
            phone_number=user_data.phone_number,
            company_id=company_id,
            role=user_data.role,
        )
        user = await user_service.create_user(add_user)
        logger.info("User registration attempt finished.")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=user_data.model_dump(),
    )


@router.post("/login")
async def login_for_access_token(
    login_data: Login,
    user_service: UserService = Depends(get_user_service),
    user_company: UserCompanyService = Depends(get_user_company_service),
) -> JSONResponse:  # type: ignore
    verify_password_result = False
    user = await user_service.get_user_by_email(login_data.email)
    verify_password_result = False
    if user:
        verify_password_result = verify_password(
            login_data.password, user.password_hash
        )
    if verify_password_result == True:
        subject = f"email:{user.email},id:{user.id},role:{user.role}"
        access_token = security.create_access_token(
            subject=subject,
            expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "subscription_id": user.subscription_id,
                "role": user.role,
                "company_id": user.company_id,
            },
        )
    else:
        JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Incorrect email or password"},
        )

    subject = f"email:{user.email},id:{user.id},role:{user.role}"
    access_token = security.create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "subscription_id": user.subscription_id,
            "role": user.role,
            "company_id": user.company_id,
        },
    )


@router.post("/google-auth")
async def google_auth(
    google_auth_data: GoogleAuth,
    user_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    try:
        email = security.decode_access_token(google_auth_data.token)
        user = await user_service.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        access_token = security.create_access_token(
            subject=f"email:{user.email},id:{user.id},role:{user.role}",
            expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "subscription_id": user.subscription_id,
                "role": user.role,
                "company_id": user.company_id,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
