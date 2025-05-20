"""
Configuration settings for the RAG Engine.
"""
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RAG Engine"
    DEBUG: bool = True
    
    # Service URLs
    EMBEDDING_SERVICE_URL: str = "http://localhost:8000/api/v1"
    LLM_SERVICE_URL: str = "http://localhost:8001/api/v1"
    
    # RAG settings
    MAX_CONTEXT_DOCUMENTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    PROMPT_TEMPLATE: str = """
    Answer the following question based on the provided context.
    
    Context:
    {context}
    
    Question:
    {query}
    
    Important!
    Reply back with `I Don't know` if no relevant context found or question is asked from outside the scope of the context.
    
    Answer:
    """
    
    # Model settings
    DEFAULT_LLM_MODEL: str = "gemini-2.0-flash"
    DEFAULT_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    DEFAULT_COLLECTION_NAME: str = "documents"
    
    # Performance settings
    BATCH_SIZE: int = 32
    MAX_CONCURRENT_REQUESTS: int = 10
    TIMEOUT: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "rag_engine.log"
    
    # LLM options
    DEFAULT_LLM_OPTIONS: Dict[str, Any] = {
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.95,
        "top_k": 40
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
