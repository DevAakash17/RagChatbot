"""
Error handling utilities for the LLM service.
"""
from typing import Dict, Any, Optional


class LLMServiceError(Exception):
    """Base exception for LLM service errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ModelNotFoundError(LLMServiceError):
    """Raised when the requested model is not found."""
    
    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' not found",
            status_code=404,
            details={"model_name": model_name}
        )


class ModelRequestError(LLMServiceError):
    """Raised when there's an error in the model request."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )


class ModelResponseError(LLMServiceError):
    """Raised when there's an error in the model response."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )
