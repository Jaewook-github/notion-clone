# backend/app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, pages, databases

api_router = APIRouter()
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(pages.router, prefix="/pages", tags=["pages"])
api_router.include_router(databases.router, prefix="/databases", tags=["databases"])

# backend/app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 설정
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)