"""
Pydantic models for the Chunker Service API.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union


class ChunkDocumentRequest(BaseModel):
    """Request model for chunking a document."""

    document_path: str = Field(..., description="Path to the document in storage")
    collection_name: Optional[str] = Field(None, description="Name of the collection to store embeddings")
    chunking_strategy: Optional[str] = Field(None, description="Chunking strategy to use")
    chunking_params: Optional[Dict[str, Any]] = Field(None, description="Additional parameters for the chunking strategy")
    embedding_model: Optional[str] = Field(None, description="Embedding model to use")
    storage_type: Optional[str] = Field(None, description="Storage type to use")
    storage_params: Optional[Dict[str, Any]] = Field(None, description="Additional parameters for the storage adapter")
    document_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the document")


class ChunkCollectionRequest(BaseModel):
    """Request model for chunking a collection of documents."""

    collection_path: str = Field(..., description="Path to the collection in storage")
    vector_collection_name: Optional[str] = Field(None, description="Name of the collection to store embeddings")
    chunking_strategy: Optional[str] = Field(None, description="Chunking strategy to use")
    chunking_params: Optional[Dict[str, Any]] = Field(None, description="Additional parameters for the chunking strategy")
    embedding_model: Optional[str] = Field(None, description="Embedding model to use")
    storage_type: Optional[str] = Field(None, description="Storage type to use")
    storage_params: Optional[Dict[str, Any]] = Field(None, description="Additional parameters for the storage adapter")
    collection_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the collection")
    file_extensions: Optional[List[str]] = Field(None, description="List of file extensions to process")


class ChunkDocumentResponse(BaseModel):
    """Response model for chunking a document."""

    document_path: str = Field(..., description="Path to the document")
    collection_name: str = Field(..., description="Name of the collection")
    chunk_count: int = Field(..., description="Number of chunks")
    chunk_ids: List[str] = Field(..., description="IDs of the chunks")
    chunking_strategy: str = Field(..., description="Chunking strategy used")
    chunking_config: Dict[str, Any] = Field(..., description="Chunking strategy configuration")
    already_processed: Optional[bool] = Field(False, description="Whether the document was already processed")


class ChunkCollectionResponse(BaseModel):
    """Response model for chunking a collection of documents."""

    collection_path: str = Field(..., description="Path to the collection")
    vector_collection_name: str = Field(..., description="Name of the vector collection")
    document_count: int = Field(..., description="Number of documents processed")
    chunk_count: int = Field(..., description="Total number of chunks")
    documents: List[ChunkDocumentResponse] = Field(..., description="Results for each document")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Service status")
    embedding_service: bool = Field(..., description="Embedding service status")


class ErrorResponse(BaseModel):
    """Response model for errors."""

    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
