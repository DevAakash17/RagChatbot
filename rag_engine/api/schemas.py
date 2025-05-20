"""
API schemas for the RAG Engine.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    """Token usage information."""
    
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens used")


class ContextDocument(BaseModel):
    """Context document information."""
    
    id: str = Field(..., description="Document ID")
    text: str = Field(..., description="Document text")
    score: float = Field(..., description="Similarity score")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")


class QueryRequest(BaseModel):
    """Request schema for querying the RAG Engine."""
    
    query: str = Field(..., description="User query")
    collection_name: Optional[str] = Field(None, description="Name of the collection to query")
    llm_model: Optional[str] = Field(None, description="LLM model to use")
    embedding_model: Optional[str] = Field(None, description="Embedding model to use")
    llm_options: Optional[Dict[str, Any]] = Field(None, description="LLM generation options")
    top_k: Optional[int] = Field(None, description="Number of context documents to retrieve")


class QueryResponse(BaseModel):
    """Response schema for RAG Engine queries."""
    
    text: str = Field(..., description="Generated text")
    model: str = Field(..., description="LLM model used")
    usage: TokenUsage = Field(..., description="Token usage information")
    finish_reason: Optional[str] = Field(None, description="Reason for finishing generation")
    context_documents: List[ContextDocument] = Field(..., description="Retrieved context documents")


class StoreDocumentsRequest(BaseModel):
    """Request schema for storing documents."""
    
    texts: List[str] = Field(..., description="List of texts to store")
    collection_name: Optional[str] = Field(None, description="Name of the collection")
    metadata: Optional[List[Dict[str, Any]]] = Field(None, description="Optional metadata for each text")
    model: Optional[str] = Field(None, description="Embedding model to use")


class StoreDocumentsResponse(BaseModel):
    """Response schema for storing documents."""
    
    ids: List[str] = Field(..., description="List of document IDs")
    collection_name: str = Field(..., description="Name of the collection")
    count: int = Field(..., description="Number of documents stored")


class CollectionInfo(BaseModel):
    """Collection information."""
    
    name: str = Field(..., description="Collection name")
    count: int = Field(..., description="Number of documents in the collection")
    dimension: int = Field(..., description="Dimension of the embeddings")


class ListCollectionsResponse(BaseModel):
    """Response schema for listing collections."""
    
    collections: List[CollectionInfo] = Field(..., description="List of collections")


class HealthResponse(BaseModel):
    """Response schema for health check."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    message: str = Field(..., description="Error message")
    details: Dict[str, Any] = Field({}, description="Error details")
