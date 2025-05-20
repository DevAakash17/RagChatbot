"""
API routes for the Chunker Service.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from chatbot.chunker_service.api.schemas import (
    ChunkDocumentRequest,
    ChunkDocumentResponse,
    ChunkCollectionRequest,
    ChunkCollectionResponse,
    HealthResponse,
    ErrorResponse
)
from chatbot.chunker_service.core.errors import ChunkerServiceError
from chatbot.chunker_service.core.logging import setup_logging
from chatbot.chunker_service.services.chunker_service import ChunkerService
from chatbot.chunker_service.services.embedding_client import EmbeddingClient


logger = setup_logging(__name__)
router = APIRouter()


# Dependency to get the chunker service
def get_chunker_service() -> ChunkerService:
    """Get the chunker service.
    
    Returns:
        Chunker service instance
    """
    return ChunkerService()


@router.post(
    "/chunk",
    response_model=ChunkDocumentResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Chunk a document",
    description="Chunk a document from storage and store embeddings in the vector database"
)
async def chunk_document(
    request: ChunkDocumentRequest,
    service: ChunkerService = Depends(get_chunker_service)
):
    """Chunk a document."""
    try:
        result = await service.chunk_document(
            document_path=request.document_path,
            collection_name=request.collection_name,
            chunking_strategy=request.chunking_strategy,
            chunking_params=request.chunking_params,
            embedding_model=request.embedding_model,
            storage_type=request.storage_type,
            storage_params=request.storage_params,
            document_metadata=request.document_metadata
        )
        
        return ChunkDocumentResponse(**result)
    except ChunkerServiceError as e:
        logger.error(f"Error chunking document: {e.message}")
        raise e.to_http_exception()
    except Exception as e:
        logger.error(f"Unexpected error chunking document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "details": {"error": str(e)}}
        )


@router.post(
    "/chunk/collection",
    response_model=ChunkCollectionResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Chunk a collection of documents",
    description="Chunk a collection of documents from storage and store embeddings in the vector database"
)
async def chunk_collection(
    request: ChunkCollectionRequest,
    service: ChunkerService = Depends(get_chunker_service)
):
    """Chunk a collection of documents."""
    try:
        result = await service.chunk_collection(
            collection_path=request.collection_path,
            vector_collection_name=request.vector_collection_name,
            chunking_strategy=request.chunking_strategy,
            chunking_params=request.chunking_params,
            embedding_model=request.embedding_model,
            storage_type=request.storage_type,
            storage_params=request.storage_params,
            collection_metadata=request.collection_metadata,
            file_extensions=request.file_extensions
        )
        
        return ChunkCollectionResponse(**result)
    except ChunkerServiceError as e:
        logger.error(f"Error chunking collection: {e.message}")
        raise e.to_http_exception()
    except Exception as e:
        logger.error(f"Unexpected error chunking collection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "details": {"error": str(e)}}
        )


@router.get(
    "/collections",
    response_model=List[Dict[str, Any]],
    responses={
        500: {"model": ErrorResponse}
    },
    summary="List collections",
    description="List all collections in the vector database"
)
async def list_collections(
    service: ChunkerService = Depends(get_chunker_service)
):
    """List collections."""
    try:
        return await service.list_collections()
    except ChunkerServiceError as e:
        logger.error(f"Error listing collections: {e.message}")
        raise e.to_http_exception()
    except Exception as e:
        logger.error(f"Unexpected error listing collections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "details": {"error": str(e)}}
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health of the service"
)
async def health_check(
    service: ChunkerService = Depends(get_chunker_service)
):
    """Health check."""
    # Check embedding service
    embedding_client = EmbeddingClient()
    embedding_service_healthy = await embedding_client.health_check()
    
    return HealthResponse(
        status="ok",
        embedding_service=embedding_service_healthy
    )
