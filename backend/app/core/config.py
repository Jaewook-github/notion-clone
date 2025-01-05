# backend/app/core/config.py
from pydantic import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Notion Clone"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 간단한 접근 제어
    ALLOWED_IPS: List[str] = ["127.0.0.1", "192.168.0.0/24"]  # 로컬호스트 및 내부 네트워크
    ADMIN_PASSWORD: str = "your-secret-password"  # 간단한 관리자 비밀번호

    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./notion_clone.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
