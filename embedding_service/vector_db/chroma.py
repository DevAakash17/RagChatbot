"""
ChromaDB implementation of the vector database.
"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple, Union
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
            # For ChromaDB 1.0.x, we need to use a different approach for setting distance function
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"dimension": dimension}
            )

            # Try to set the distance function if possible
            try:
                # For ChromaDB 1.0.x, we can try to access the underlying collection settings
                if hasattr(collection, '_embedding_function') and hasattr(collection, '_distance_function'):
                    # Some versions allow setting these attributes directly
                    collection._distance_function = "cosine"
                    logger.info(f"Set distance function to 'cosine' for collection '{collection_name}'")
                elif hasattr(collection, 'set_distance_function'):
                    # Some versions have a setter method
                    collection.set_distance_function("cosine")
                    logger.info(f"Set distance function to 'cosine' for collection '{collection_name}'")
            except Exception as e:
                # If we can't set the distance function, just log it and continue
                logger.warning(f"Could not set distance function for collection '{collection_name}': {str(e)}")

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
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[List[Dict[str, Any]]]:
        """Search for similar vectors with improved formatting and filtering.

        Args:
            collection_name: Name of the collection
            query_vectors: List of query vectors
            top_k: Number of results to return
            filter_dict: Optional metadata filter dictionary

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
                # Prepare query parameters for ChromaDB 1.0.x
                # In 1.0.x, the API changed significantly
                include_fields = ["documents", "metadatas", "distances"]

                # Try to include embeddings if supported
                try:
                    # Test if embeddings are supported
                    test_query = collection.query(
                        query_embeddings=[query_vector[:5]],  # Just use first few dimensions for test
                        n_results=1,
                        include=["embeddings"]
                    )
                    # If we get here, embeddings are supported
                    include_fields.append("embeddings")
                    logger.debug("Including embeddings in query results")
                except Exception:
                    # Embeddings not supported, continue without them
                    logger.debug("Embeddings not included in query results (not supported)")

                query_params = {
                    "query_embeddings": [query_vector],
                    "n_results": top_k,
                    "include": include_fields
                }

                # Add filter if provided
                if filter_dict:
                    query_params["where"] = filter_dict

                # Execute query
                query_result = collection.query(**query_params)

                # Format results with improved scoring
                formatted_results = []

                # Check if we have any results
                if query_result["ids"] and len(query_result["ids"]) > 0 and len(query_result["ids"][0]) > 0:
                    for i in range(len(query_result["ids"][0])):
                        # Get the raw distance
                        distance = query_result["distances"][0][i] if "distances" in query_result and query_result["distances"] else 0.0

                        # Convert distance to similarity score (cosine distance to similarity)
                        # For cosine distance: similarity = 1 - distance
                        similarity_score = 1.0 - distance

                        # Get metadata safely
                        metadata = {}
                        if "metadatas" in query_result and query_result["metadatas"] and len(query_result["metadatas"]) > 0:
                            metadata = query_result["metadatas"][0][i] or {}

                        # Create result entry with more information
                        result_entry = {
                            "id": query_result["ids"][0][i],
                            "text": query_result["documents"][0][i] if "documents" in query_result and query_result["documents"] else "",
                            "score": similarity_score,
                            "raw_distance": distance,
                            "metadata": metadata
                        }

                        # Add embeddings if available
                        if "embeddings" in query_result and query_result["embeddings"] and len(query_result["embeddings"]) > 0:
                            result_entry["embedding"] = query_result["embeddings"][0][i]

                        formatted_results.append(result_entry)

                # Sort by score in descending order
                formatted_results = sorted(formatted_results, key=lambda x: x["score"], reverse=True)
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
