"""
Configuration settings for the Embedding Service.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Embedding Service"
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Default model
    EMBEDDING_DIMENSION: int = 384  # Dimension for the default model
    
    # Vector DB settings
    VECTOR_DB_TYPE: str = "chroma"  # Options: "chroma", "faiss"
    VECTOR_DB_PATH: str = "./vector_db_data"  # Local storage path
    
    # Performance settings
    BATCH_SIZE: int = 32
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "embedding_service.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
