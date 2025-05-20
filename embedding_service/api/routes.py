"""
API routes for the Embedding Service.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from ..core.errors import EmbeddingServiceError
from ..models.schemas import (
    TextEmbeddingRequest,
    TextEmbeddingResponse,
    StoreEmbeddingRequest,
    StoreEmbeddingResponse,
    QueryRequest,
    QueryResponse,
    QueryResult,
    ListCollectionsResponse,
    CollectionInfo,
    DeleteCollectionRequest,
    DeleteCollectionResponse,
    HealthResponse
)
from ..services.embedding_service import EmbeddingService


# Create router
router = APIRouter()

# Create embedding service instance
embedding_service = EmbeddingService()


def get_embedding_service() -> EmbeddingService:
    """Get the embedding service instance.
    
    Returns:
        Embedding service instance
    """
    return embedding_service


@router.post(
    "/embeddings",
    response_model=TextEmbeddingResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate embeddings for texts",
    description="Generate embeddings for a list of texts using the specified model."
)
async def generate_embeddings(
    request: TextEmbeddingRequest,
    service: EmbeddingService = Depends(get_embedding_service)
):
    """Generate embeddings for texts."""
    try:
        embeddings, model_name, dimension = service.generate_embeddings(
            texts=request.texts,
            model_name=request.model
        )
        
        return TextEmbeddingResponse(
            embeddings=embeddings,
            model=model_name,
            dimension=dimension
        )
    except EmbeddingServiceError as e:
        raise e.to_http_exception()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to generate embeddings: {str(e)}"}
        )


@router.post(
    "/collections/store",
    response_model=StoreEmbeddingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Store embeddings in a collection",
    description="Generate embeddings for texts and store them in the specified collection."
)
async def store_embeddings(
    request: StoreEmbeddingRequest,
    service: EmbeddingService = Depends(get_embedding_service)
):
    """Store embeddings in a collection."""
    try:
        ids, collection_name, count = service.store_embeddings(
            texts=request.texts,
            collection_name=request.collection_name,
            metadata=request.metadata,
            model_name=request.model
        )
        
        return StoreEmbeddingResponse(
            ids=ids,
            collection_name=collection_name,
            count=count
        )
    except EmbeddingServiceError as e:
        raise e.to_http_exception()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to store embeddings: {str(e)}"}
        )


@router.post(
    "/collections/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query for similar embeddings",
    description="Query for embeddings similar to the query texts in the specified collection."
)
async def query_similar(
    request: QueryRequest,
    service: EmbeddingService = Depends(get_embedding_service)
):
    """Query for similar embeddings."""
    try:
        results, collection_name = service.query_similar(
            query_texts=request.query_texts,
            collection_name=request.collection_name,
            top_k=request.top_k,
            model_name=request.model
        )
        
        # Convert to response model
        query_results = []
        for result_list in results:
            query_result = [
                QueryResult(
                    id=item["id"],
                    text=item["text"],
                    score=item["score"],
                    metadata=item["metadata"]
                )
                for item in result_list
            ]
            query_results.append(query_result)
        
        return QueryResponse(
            results=query_results,
            collection_name=collection_name
        )
    except EmbeddingServiceError as e:
        raise e.to_http_exception()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to query similar embeddings: {str(e)}"}
        )


@router.get(
    "/collections",
    response_model=ListCollectionsResponse,
    status_code=status.HTTP_200_OK,
    summary="List collections",
    description="List all collections in the vector database."
)
async def list_collections(
    service: EmbeddingService = Depends(get_embedding_service)
):
    """List collections."""
    try:
        collections = service.list_collections()
        
        # Convert to response model
        collection_infos = [
            CollectionInfo(
                name=collection["name"],
                count=collection["count"],
                dimension=collection["dimension"]
            )
            for collection in collections
        ]
        
        return ListCollectionsResponse(collections=collection_infos)
    except EmbeddingServiceError as e:
        raise e.to_http_exception()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to list collections: {str(e)}"}
        )


@router.post(
    "/collections/delete",
    response_model=DeleteCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a collection",
    description="Delete a collection from the vector database."
)
async def delete_collection(
    request: DeleteCollectionRequest,
    service: EmbeddingService = Depends(get_embedding_service)
):
    """Delete a collection."""
    try:
        success = service.delete_collection(request.collection_name)
        
        return DeleteCollectionResponse(
            collection_name=request.collection_name,
            success=success
        )
    except EmbeddingServiceError as e:
        raise e.to_http_exception()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to delete collection: {str(e)}"}
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health of the service."
)
async def health_check(
    service: EmbeddingService = Depends(get_embedding_service)
):
    """Health check."""
    try:
        health_info = service.get_health_info()
        
        return HealthResponse(**health_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Health check failed: {str(e)}"}
        )
