"""
Pydantic models for the Embedding Service.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union, Any


class TextEmbeddingRequest(BaseModel):
    """Request model for text embedding generation."""
    
    texts: List[str] = Field(..., min_items=1, description="List of texts to embed")
    model: Optional[str] = Field(None, description="Embedding model to use")
    
    @validator('texts')
    def validate_texts(cls, texts):
        if not all(isinstance(text, str) for text in texts):
            raise ValueError("All items in 'texts' must be strings")
        if not all(text.strip() for text in texts):
            raise ValueError("Empty strings are not allowed in 'texts'")
        return texts


class TextEmbeddingResponse(BaseModel):
    """Response model for text embedding generation."""
    
    embeddings: List[List[float]] = Field(..., description="List of embeddings")
    model: str = Field(..., description="Embedding model used")
    dimension: int = Field(..., description="Dimension of embeddings")


class StoreEmbeddingRequest(BaseModel):
    """Request model for storing embeddings in the vector database."""
    
    texts: List[str] = Field(..., min_items=1, description="List of texts to embed and store")
    metadata: Optional[List[Dict[str, Any]]] = Field(None, description="Metadata for each text")
    collection_name: str = Field(..., description="Name of the collection to store embeddings")
    model: Optional[str] = Field(None, description="Embedding model to use")
    
    @validator('metadata')
    def validate_metadata(cls, metadata, values):
        if metadata and 'texts' in values and len(metadata) != len(values['texts']):
            raise ValueError("Length of metadata must match length of texts")
        return metadata


class StoreEmbeddingResponse(BaseModel):
    """Response model for storing embeddings."""
    
    ids: List[str] = Field(..., description="IDs of stored embeddings")
    collection_name: str = Field(..., description="Name of the collection")
    count: int = Field(..., description="Number of embeddings stored")


class QueryRequest(BaseModel):
    """Request model for querying similar embeddings."""
    
    query_texts: List[str] = Field(..., min_items=1, description="List of query texts")
    collection_name: str = Field(..., description="Name of the collection to query")
    top_k: int = Field(5, ge=1, le=100, description="Number of results to return")
    model: Optional[str] = Field(None, description="Embedding model to use")


class QueryResult(BaseModel):
    """Model for a single query result."""
    
    id: str = Field(..., description="ID of the embedding")
    text: str = Field(..., description="Original text")
    score: float = Field(..., description="Similarity score")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata associated with the embedding")


class QueryResponse(BaseModel):
    """Response model for querying similar embeddings."""
    
    results: List[List[QueryResult]] = Field(..., description="List of results for each query")
    collection_name: str = Field(..., description="Name of the collection queried")


class CollectionInfo(BaseModel):
    """Model for collection information."""
    
    name: str = Field(..., description="Name of the collection")
    count: int = Field(..., description="Number of embeddings in the collection")
    dimension: int = Field(..., description="Dimension of embeddings")


class ListCollectionsResponse(BaseModel):
    """Response model for listing collections."""
    
    collections: List[CollectionInfo] = Field(..., description="List of collections")


class DeleteCollectionRequest(BaseModel):
    """Request model for deleting a collection."""
    
    collection_name: str = Field(..., description="Name of the collection to delete")


class DeleteCollectionResponse(BaseModel):
    """Response model for deleting a collection."""
    
    collection_name: str = Field(..., description="Name of the deleted collection")
    success: bool = Field(..., description="Whether the deletion was successful")


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Status of the service")
    version: str = Field(..., description="Version of the service")
    embedding_model: str = Field(..., description="Current embedding model")
    vector_db: str = Field(..., description="Current vector database")
