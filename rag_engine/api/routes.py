"""
API routes for the RAG Engine.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from rag_engine.api.schemas import (
    QueryRequest,
    QueryResponse,
    StoreDocumentsRequest,
    StoreDocumentsResponse,
    ListCollectionsResponse,
    CollectionInfo,
    HealthResponse,
    ContextDocument,
    TokenUsage
)
from rag_engine.services.rag_service import RAGService
from rag_engine.utils.errors import RAGEngineError
from rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)

# Create router
router = APIRouter()

# Create RAG service instance
rag_service = RAGService()


def get_rag_service() -> RAGService:
    """Get the RAG service instance.

    Returns:
        RAG service instance
    """
    return rag_service


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query the RAG Engine",
    description="Process a query through the RAG pipeline."
)
async def query(
    request: QueryRequest,
    service: RAGService = Depends(get_rag_service)
):
    """Query the RAG Engine."""
    try:
        result = await service.process_query(
            query=request.query,
            collection_name=request.collection_name,
            llm_model=request.llm_model,
            embedding_model=request.embedding_model,
            llm_options=request.llm_options,
            top_k=request.top_k,
            prev_queries=request.prev_queries
        )

        # Convert context documents to the response schema
        context_documents = [
            ContextDocument(
                id=doc["id"],
                text=doc["text"],
                score=doc["score"],
                metadata=doc.get("metadata")
            )
            for doc in result["context_documents"]
        ]

        return QueryResponse(
            text=result["text"],
            model=result["model"],
            usage=TokenUsage(**result["usage"]),
            finish_reason=result.get("finish_reason"),
            context_documents=context_documents
        )
    except RAGEngineError as e:
        raise e.to_http_exception()
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to process query: {str(e)}"}
        )


@router.post(
    "/store",
    response_model=StoreDocumentsResponse,
    status_code=status.HTTP_200_OK,
    summary="Store documents",
    description="Store documents in the vector database."
)
async def store_documents(
    request: StoreDocumentsRequest,
    service: RAGService = Depends(get_rag_service)
):
    """Store documents."""
    try:
        result = await service.store_documents(
            texts=request.texts,
            collection_name=request.collection_name,
            metadata=request.metadata,
            model=request.model
        )

        return StoreDocumentsResponse(
            ids=result["ids"],
            collection_name=result["collection_name"],
            count=result["count"]
        )
    except RAGEngineError as e:
        raise e.to_http_exception()
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to store documents: {str(e)}"}
        )


@router.get(
    "/collections",
    response_model=ListCollectionsResponse,
    status_code=status.HTTP_200_OK,
    summary="List collections",
    description="List all collections in the vector database."
)
async def list_collections(
    service: RAGService = Depends(get_rag_service)
):
    """List collections."""
    try:
        collections = await service.list_collections()

        # Convert to response schema
        collection_infos = [
            CollectionInfo(
                name=collection["name"],
                count=collection["count"],
                dimension=collection["dimension"]
            )
            for collection in collections
        ]

        return ListCollectionsResponse(collections=collection_infos)
    except RAGEngineError as e:
        raise e.to_http_exception()
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Failed to list collections: {str(e)}"}
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health of the RAG Engine."
)
async def health_check(
    service: RAGService = Depends(get_rag_service)
):
    """Health check."""
    try:
        health_info = await service.get_health_info()

        return HealthResponse(**health_info)
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Health check failed: {str(e)}"}
        )
