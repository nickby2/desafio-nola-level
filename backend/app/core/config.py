"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Analytics API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://challenge:challenge_2024@localhost:5432/challenge_db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutes
    
    # Query Performance
    MAX_QUERY_RESULTS: int = 10000
    QUERY_TIMEOUT_SECONDS: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
