"""
API schemas for request and response validation.
"""
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field


class GenerateTextRequest(BaseModel):
    """Request schema for text generation."""
    
    prompt: str = Field(..., description="Input prompt for text generation")
    model: str = Field("gemini-2.0-flash", description="Model to use for generation")
    options: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional options for generation"
    )


class TokenUsage(BaseModel):
    """Token usage information."""
    
    prompt_tokens: int = Field(0, description="Number of tokens in the prompt")
    completion_tokens: int = Field(0, description="Number of tokens in the completion")
    total_tokens: int = Field(0, description="Total number of tokens used")


class GenerateTextResponse(BaseModel):
    """Response schema for text generation."""
    
    text: str = Field(..., description="Generated text")
    model: str = Field(..., description="Model used for generation")
    usage: TokenUsage = Field(..., description="Token usage information")
    finish_reason: Optional[str] = Field(None, description="Reason for finishing generation")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Status of the service")
    version: str = Field(..., description="Version of the service")
    embedding_model: str = Field(..., description="Current embedding model")
    vector_db: str = Field(..., description="Current vector database")
