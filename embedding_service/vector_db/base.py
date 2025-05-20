"""
Base class for vector databases.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple


class BaseVectorDB(ABC):
    """Abstract base class for vector databases."""
    
    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the vector database.
        
        Args:
            **kwargs: Database-specific parameters
        """
        pass
    
    @abstractmethod
    def create_collection(self, collection_name: str, dimension: int) -> bool:
        """Create a new collection.
        
        Args:
            collection_name: Name of the collection
            dimension: Dimension of the vectors
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections.
        
        Returns:
            List of collection information
        """
        pass
    
    @abstractmethod
    def add_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add vectors to a collection.
        
        Args:
            collection_name: Name of the collection
            vectors: List of vectors to add
            texts: Original texts for the vectors
            metadata: Optional metadata for each vector
            ids: Optional IDs for the vectors
            
        Returns:
            List of IDs for the added vectors
        """
        pass
    
    @abstractmethod
    def search(
        self,
        collection_name: str,
        query_vectors: List[List[float]],
        top_k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """Search for similar vectors.
        
        Args:
            collection_name: Name of the collection
            query_vectors: List of query vectors
            top_k: Number of results to return
            
        Returns:
            List of lists of results (for each query vector)
        """
        pass
    
    @abstractmethod
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get information about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection information
        """
        pass
    
    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if the collection exists, False otherwise
        """
        pass
