"""
Configuration settings for the LLM service.
"""
import os
from typing import Dict, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "LLM Service"
    DEBUG: bool = True
    
    # LLM Model settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Model configurations
    MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
        "gemini-2.0-flash": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            "api_key_param": "key",
            "timeout": 30,
            "max_tokens": 1024,
        }
    }
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
