"""
Error handling utilities for the RAG Engine.
"""
from typing import Dict, Any, Optional
from fastapi import HTTPException, status


class RAGEngineError(Exception):
    """Base exception for RAG Engine errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        """Initialize the exception.
        
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException.
        
        Returns:
            HTTPException instance
        """
        return HTTPException(
            status_code=self.status_code,
            detail={"message": self.message, "details": self.details}
        )


class ConfigurationError(RAGEngineError):
    """Error raised when there's a configuration issue."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ServiceConnectionError(RAGEngineError):
    """Error raised when there's an issue connecting to a service."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


class EmbeddingServiceError(RAGEngineError):
    """Error raised when there's an issue with the embedding service."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class LLMServiceError(RAGEngineError):
    """Error raised when there's an issue with the LLM service."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class ValidationError(RAGEngineError):
    """Error raised when there's a validation issue."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class ResourceNotFoundError(RAGEngineError):
    """Error raised when a resource is not found."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )
