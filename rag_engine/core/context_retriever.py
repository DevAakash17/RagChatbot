"""
Context retriever for the RAG Engine.
"""
from typing import List, Dict, Any, Optional

from chatbot.rag_engine.core.config import settings
from chatbot.rag_engine.services.embedding_client import EmbeddingClient
from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class ContextRetriever:
    """Retrieves relevant context using embeddings."""
    
    def __init__(self, embedding_client: Optional[EmbeddingClient] = None):
        """Initialize the context retriever.
        
        Args:
            embedding_client: Optional embedding client
        """
        self.embedding_client = embedding_client or EmbeddingClient()
        logger.info("Initialized ContextRetriever")
    
    async def retrieve_context(
        self,
        query: str,
        collection_name: Optional[str] = None,
        top_k: Optional[int] = None,
        model: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query.
        
        Args:
            query: User query
            collection_name: Name of the collection to query
            top_k: Number of results to return
            model: Optional model name to use
            
        Returns:
            List of relevant documents
        """
        collection = collection_name or settings.DEFAULT_COLLECTION_NAME
        k = top_k or settings.MAX_CONTEXT_DOCUMENTS
        
        logger.info(f"Retrieving context for query: {query}")
        
        # Query the embedding service
        results = await self.embedding_client.query_collection(
            query_text=query,
            collection_name=collection,
            top_k=k,
            model=model
        )
        
        # Filter results by similarity threshold
        filtered_results = [
            result for result in results
            if result["score"] >= settings.SIMILARITY_THRESHOLD
        ]
        
        logger.info(f"Retrieved {len(filtered_results)} relevant documents")
        return filtered_results
