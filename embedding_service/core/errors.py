"""
Error handling for the Embedding Service.
"""
from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class EmbeddingServiceError(Exception):
    """Base exception for Embedding Service."""
    
    def __init__(
        self, 
        message: str = "An error occurred in the Embedding Service",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException."""
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "details": self.details
            }
        )


class EmbeddingModelError(EmbeddingServiceError):
    """Exception raised for errors in the embedding model."""
    
    def __init__(
        self, 
        message: str = "Error with embedding model",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class VectorDBError(EmbeddingServiceError):
    """Exception raised for errors in the vector database."""
    
    def __init__(
        self, 
        message: str = "Error with vector database",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ValidationError(EmbeddingServiceError):
    """Exception raised for validation errors."""
    
    def __init__(
        self, 
        message: str = "Validation error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class ResourceNotFoundError(EmbeddingServiceError):
    """Exception raised when a resource is not found."""
    
    def __init__(
        self, 
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )
