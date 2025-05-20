"""
Configuration settings for the Chunker Service.
"""
from typing import Dict, Any, Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chunker Service"
    DEBUG: bool = True

    # Service URLs
    EMBEDDING_SERVICE_URL: str = "http://localhost:8000/api/v1"

    # Storage settings
    STORAGE_TYPE: str = "local"  # Options: "local", "s3"
    STORAGE_BASE_PATH: str = "./storage_data"  # For local storage

    # S3 settings (only used if STORAGE_TYPE is "s3")
    S3_ENDPOINT: Optional[str] = None  # For custom S3-compatible services
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_REGION: str = "us-east-1"

    # Chunking settings
    DEFAULT_CHUNK_SIZE: int = 1000  # Characters
    DEFAULT_CHUNK_OVERLAP: int = 200  # Characters
    DEFAULT_CHUNKING_STRATEGY: str = "fixed_size"  # Options: "fixed_size", "semantic"

    # Embedding settings
    DEFAULT_EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    DEFAULT_COLLECTION_NAME: str = "insurance_documents"

    # Performance settings
    BATCH_SIZE: int = 32
    MAX_CONCURRENT_REQUESTS: int = 10
    TIMEOUT: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "chunker_service.log"

    # MongoDB settings
    MONGODB_CONNECTION_STRING: str = "mongodb://localhost:27017"
    MONGODB_DATABASE_NAME: str = "chunker_service"
    MONGODB_DOCUMENT_COLLECTION: str = "processed_documents"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
