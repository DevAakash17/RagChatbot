"""
RAG service implementation.
"""
from typing import Dict, Any, Optional, List

from rag_engine.core.config import settings
from rag_engine.core.engine import RAGEngine
from rag_engine.services.embedding_client import EmbeddingClient
from rag_engine.services.llm_client import LLMClient
from rag_engine.utils.errors import ValidationError, ResourceNotFoundError
from rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class RAGService:
    """Service for RAG operations."""

    def __init__(
        self,
        embedding_client: Optional[EmbeddingClient] = None,
        llm_client: Optional[LLMClient] = None
    ):
        """Initialize the RAG service.

        Args:
            embedding_client: Optional embedding client
            llm_client: Optional LLM client
        """
        # Initialize clients
        self.embedding_client = embedding_client or EmbeddingClient()
        self.llm_client = llm_client or LLMClient()

        # Initialize RAG engine
        self.engine = RAGEngine(
            embedding_client=self.embedding_client,
            llm_client=self.llm_client
        )

        logger.info("Initialized RAGService")

    async def process_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        llm_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        llm_options: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None,
        prev_queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Process a query through the RAG pipeline.

        Args:
            query: User query
            collection_name: Name of the collection to query
            llm_model: Optional LLM model to use
            embedding_model: Optional embedding model to use
            llm_options: Optional LLM generation options
            top_k: Number of context documents to retrieve
            prev_queries: Optional list of previous queries for context

        Returns:
            Generated response and metadata
        """
        # Validate query
        if not query or not query.strip():
            raise ValidationError(message="Query cannot be empty")

        # Use default collection if not specified
        collection = collection_name or settings.DEFAULT_COLLECTION_NAME

        # Check if collection exists
        collections = await self.embedding_client.list_collections()
        collection_names = [c["name"] for c in collections]

        if collection not in collection_names:
            raise ResourceNotFoundError(
                message=f"Collection '{collection}' not found",
                details={"available_collections": collection_names}
            )

        # Process the query
        response = await self.engine.process(
            query=query,
            collection_name=collection,
            llm_model=llm_model,
            embedding_model=embedding_model,
            llm_options=llm_options,
            top_k=top_k,
            prev_queries=prev_queries or []
        )

        return response

    async def store_documents(
        self,
        texts: List[str],
        collection_name: Optional[str] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Store documents in the vector database.

        Args:
            texts: List of texts to store
            collection_name: Name of the collection
            metadata: Optional metadata for each text
            model: Optional embedding model to use

        Returns:
            Storage result
        """
        # Validate texts
        if not texts:
            raise ValidationError(message="Texts list cannot be empty")

        # Use default collection if not specified
        collection = collection_name or settings.DEFAULT_COLLECTION_NAME

        # Store documents
        ids, collection_name, count = await self.embedding_client.store_embeddings(
            texts=texts,
            collection_name=collection,
            metadata=metadata,
            model=model
        )

        return {
            "ids": ids,
            "collection_name": collection_name,
            "count": count
        }

    async def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections.

        Returns:
            List of collections
        """
        return await self.embedding_client.list_collections()

    async def get_health_info(self) -> Dict[str, Any]:
        """Get health information.

        Returns:
            Health information
        """
        # This is a simple health check
        # In a real implementation, this would check the health of all components
        return {
            "status": "ok",
            "service": "rag_engine",
            "version": "0.1.0"
        }
