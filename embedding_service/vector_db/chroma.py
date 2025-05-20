"""
ChromaDB implementation of the vector database.
"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

from .base import BaseVectorDB
from ..core.errors import VectorDBError


class ChromaVectorDB(BaseVectorDB):
    """ChromaDB implementation of the vector database."""
    
    def __init__(self, persist_directory: str = "./vector_db_data", **kwargs):
        """Initialize the ChromaDB database.
        
        Args:
            persist_directory: Directory to persist the database
            **kwargs: Additional database parameters
        """
        try:
            import chromadb
            
            self.persist_directory = persist_directory
            
            # Create directory if it doesn't exist
            os.makedirs(persist_directory, exist_ok=True)
            
            # Initialize client
            logger.info(f"Initializing ChromaDB with persist directory: {persist_directory}")
            self.client = chromadb.PersistentClient(path=persist_directory)
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize ChromaDB: {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
    def create_collection(self, collection_name: str, dimension: int) -> bool:
        """Create a new collection.
        
        Args:
            collection_name: Name of the collection
            dimension: Dimension of the vectors
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if collection already exists
            if self.collection_exists(collection_name):
                logger.info(f"Collection '{collection_name}' already exists")
                return True
            
            # Create collection
            self.client.create_collection(
                name=collection_name,
                metadata={"dimension": dimension}
            )
            logger.info(f"Created collection '{collection_name}' with dimension {dimension}")
            return True
        except Exception as e:
            error_msg = f"Failed to create collection '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if collection exists
            if not self.collection_exists(collection_name):
                logger.warning(f"Collection '{collection_name}' does not exist")
                return False
            
            # Delete collection
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection '{collection_name}'")
            return True
        except Exception as e:
            error_msg = f"Failed to delete collection '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections.
        
        Returns:
            List of collection information
        """
        try:
            collections = self.client.list_collections()
            result = []
            
            for collection in collections:
                collection_info = self.get_collection_info(collection.name)
                result.append(collection_info)
            
            return result
        except Exception as e:
            error_msg = f"Failed to list collections: {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
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
        try:
            # Check if collection exists
            if not self.collection_exists(collection_name):
                dimension = len(vectors[0]) if vectors else 0
                self.create_collection(collection_name, dimension)
            
            # Get collection
            collection = self.client.get_collection(name=collection_name)
            
            # Generate IDs if not provided
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
            
            # Add vectors
            collection.add(
                embeddings=vectors,
                documents=texts,
                metadatas=metadata,
                ids=ids
            )
            
            logger.info(f"Added {len(vectors)} vectors to collection '{collection_name}'")
            return ids
        except Exception as e:
            error_msg = f"Failed to add vectors to collection '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
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
        try:
            # Check if collection exists
            if not self.collection_exists(collection_name):
                error_msg = f"Collection '{collection_name}' does not exist"
                logger.error(error_msg)
                raise VectorDBError(message=error_msg)
            
            # Get collection
            collection = self.client.get_collection(name=collection_name)
            
            # Search for each query vector
            results = []
            for query_vector in query_vectors:
                query_result = collection.query(
                    query_embeddings=[query_vector],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                # Format results
                formatted_results = []
                for i in range(len(query_result["ids"][0])):
                    formatted_results.append({
                        "id": query_result["ids"][0][i],
                        "text": query_result["documents"][0][i],
                        "score": 1.0 - query_result["distances"][0][i],  # Convert distance to similarity score
                        "metadata": query_result["metadatas"][0][i]
                    })
                
                results.append(formatted_results)
            
            return results
        except Exception as e:
            error_msg = f"Failed to search in collection '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get information about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection information
        """
        try:
            # Check if collection exists
            if not self.collection_exists(collection_name):
                error_msg = f"Collection '{collection_name}' does not exist"
                logger.error(error_msg)
                raise VectorDBError(message=error_msg)
            
            # Get collection
            collection = self.client.get_collection(name=collection_name)
            
            # Get collection info
            count = collection.count()
            metadata = collection.metadata
            dimension = metadata.get("dimension", 0) if metadata else 0
            
            return {
                "name": collection_name,
                "count": count,
                "dimension": dimension
            }
        except Exception as e:
            error_msg = f"Failed to get information for collection '{collection_name}': {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
    
    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if the collection exists, False otherwise
        """
        try:
            collections = self.client.list_collections()
            return any(collection.name == collection_name for collection in collections)
        except Exception as e:
            error_msg = f"Failed to check if collection '{collection_name}' exists: {str(e)}"
            logger.error(error_msg)
            raise VectorDBError(message=error_msg)
