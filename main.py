from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Depends
from controllers import (
    auth_controller,
    payment_controller,
    user_controller,
    company_controller,
    pdf_controller,
    user_config_controller,
    master_config_controller,
    subscription_controller,
    users_dashboard_controller,
    admin_controller,  
    user_company_controller 
)
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import execute_sql_from_file, get_database
import os
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
import json
import orjson
from datetime import datetime, tzinfo


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Update this path as needed
    # await execute_sql_from_file()
    print("Starting up...")
    yield


app = FastAPI(
    host="localhost",
    port=8000,
    redirect_slashes=False,
    lifespan=lifespan,
    title="WizDocx API",
    description="API for WizDocx",
    version="1.0.0",
    default_response_class=JSONResponse,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    
)
# app.add_middleware(BaseHTTPMiddleware, dispatch=SerializeJSONMiddleware)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024
UPLOAD_DIRECTORY = "uploads"  # Store uploaded files
PROCESSED_DIRECTORY = "processed"  # Store processed files
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(payment_controller.router)
app.include_router(pdf_controller.router)
app.include_router(user_config_controller.router)
app.include_router(master_config_controller.router)
app.include_router(subscription_controller.router)
app.include_router(users_dashboard_controller.router)
app.include_router(admin_controller.router)
app.include_router(company_controller.router)
app.include_router(user_company_controller.router)