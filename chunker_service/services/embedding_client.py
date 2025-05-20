"""
Client for interacting with the Embedding Service.
"""
from typing import List, Dict, Any, Optional, Tuple
import aiohttp
from fastapi import status

from chatbot.chunker_service.core.config import settings
from chatbot.chunker_service.core.errors import EmbeddingServiceError, ServiceConnectionError
from chatbot.chunker_service.core.logging import setup_logging


logger = setup_logging(__name__)


class EmbeddingClient:
    """Client for the Embedding Service."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the client.
        
        Args:
            base_url: Base URL for the Embedding Service API
        """
        self.base_url = base_url or settings.EMBEDDING_SERVICE_URL
        logger.info(f"Initialized EmbeddingClient with base URL: {self.base_url}")
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None
    ) -> Tuple[List[List[float]], str, int]:
        """Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to embed
            model: Optional model name to use
            
        Returns:
            Tuple of (embeddings, model_name, dimension)
        """
        url = f"{self.base_url}/embeddings"
        
        payload = {
            "texts": texts,
            "model": model or settings.DEFAULT_EMBEDDING_MODEL
        }
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    json=payload,
                    timeout=settings.TIMEOUT
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Embedding Service error: {error_text}")
                        raise EmbeddingServiceError(
                            message=f"Embedding Service returned status {response.status}",
                            details={"status": response.status, "response": error_text}
                        )
                    
                    response_data = await response.json()
                    
                    return (
                        response_data["embeddings"],
                        response_data["model"],
                        response_data["dimension"]
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Failed to connect to Embedding Service: {str(e)}")
            raise ServiceConnectionError(
                message=f"Failed to connect to Embedding Service: {str(e)}",
                details={"url": url}
            )
    
    async def store_embeddings(
        self,
        texts: List[str],
        collection_name: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None
    ) -> Tuple[List[str], str, int]:
        """Store embeddings in a collection.
        
        Args:
            texts: List of texts to embed and store
            collection_name: Name of the collection
            metadata: Optional metadata for each text
            model: Optional model name to use
            
        Returns:
            Tuple of (ids, collection_name, count)
        """
        url = f"{self.base_url}/collections/store"
        
        payload = {
            "texts": texts,
            "collection_name": collection_name,
            "metadata": metadata,
            "model": model or settings.DEFAULT_EMBEDDING_MODEL
        }
        
        logger.info(f"Storing {len(texts)} texts in collection '{collection_name}'")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    json=payload,
                    timeout=settings.TIMEOUT
                ) as response:
                    if response.status != status.HTTP_201_CREATED:
                        error_text = await response.text()
                        logger.error(f"Embedding Service error: {error_text}")
                        raise EmbeddingServiceError(
                            message=f"Embedding Service returned status {response.status}",
                            details={"status": response.status, "response": error_text}
                        )
                    
                    response_data = await response.json()
                    
                    return (
                        response_data["ids"],
                        response_data["collection_name"],
                        response_data["count"]
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Failed to connect to Embedding Service: {str(e)}")
            raise ServiceConnectionError(
                message=f"Failed to connect to Embedding Service: {str(e)}",
                details={"url": url}
            )
    
    async def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections.
        
        Returns:
            List of collections
        """
        url = f"{self.base_url}/collections"
        
        logger.info("Listing collections")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    timeout=settings.TIMEOUT
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Embedding Service error: {error_text}")
                        raise EmbeddingServiceError(
                            message=f"Embedding Service returned status {response.status}",
                            details={"status": response.status, "response": error_text}
                        )
                    
                    response_data = await response.json()
                    
                    return response_data["collections"]
        except aiohttp.ClientError as e:
            logger.error(f"Failed to connect to Embedding Service: {str(e)}")
            raise ServiceConnectionError(
                message=f"Failed to connect to Embedding Service: {str(e)}",
                details={"url": url}
            )
    
    async def health_check(self) -> bool:
        """Check if the Embedding Service is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        url = f"{self.base_url}/health"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    timeout=5  # Short timeout for health check
                ) as response:
                    return response.status == 200
        except:
            return False
