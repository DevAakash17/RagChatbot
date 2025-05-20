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
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"  # Good quality model with smaller size (384 dimensions)
    EMBEDDING_DIMENSION: int = 384  # Expected dimension for the model
    FORCE_MODEL_DOWNLOAD: bool = False  # Don't force download to avoid timeouts
    MODEL_CACHE_DIR: Optional[str] = None  # Custom cache directory for models

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
