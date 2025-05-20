"""
Embedding service implementation.
"""
from typing import List, Dict, Any, Optional, Tuple, Type
from loguru import logger

from ..core.config import settings
from ..core.errors import EmbeddingServiceError, ValidationError, ResourceNotFoundError
from ..embeddings.base import BaseEmbeddingModel
from ..embeddings.sentence_transformers import SentenceTransformerModel
from ..vector_db.base import BaseVectorDB
from ..vector_db.chroma import ChromaVectorDB


class EmbeddingService:
    """Service for generating and managing embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self._embedding_model = None
        self._vector_db = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize the embedding model and vector database."""
        # Initialize embedding model
        self._embedding_model = self._create_embedding_model(
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Initialize vector database
        self._vector_db = self._create_vector_db(
            db_type=settings.VECTOR_DB_TYPE,
            persist_directory=settings.VECTOR_DB_PATH
        )
    
    def _create_embedding_model(self, model_name: str) -> BaseEmbeddingModel:
        """Create an embedding model.
        
        Args:
            model_name: Name of the model to use
            
        Returns:
            Embedding model instance
        """
        logger.info(f"Creating embedding model: {model_name}")
        
        # Currently only supporting Sentence Transformers
        return SentenceTransformerModel(model_name=model_name)
    
    def _create_vector_db(self, db_type: str, **kwargs) -> BaseVectorDB:
        """Create a vector database.
        
        Args:
            db_type: Type of vector database
            **kwargs: Additional database parameters
            
        Returns:
            Vector database instance
        """
        logger.info(f"Creating vector database: {db_type}")
        
        # Currently only supporting ChromaDB
        if db_type.lower() == "chroma":
            return ChromaVectorDB(**kwargs)
        else:
            raise ValueError(f"Unsupported vector database type: {db_type}")
    
    def generate_embeddings(
        self,
        texts: List[str],
        model_name: Optional[str] = None
    ) -> Tuple[List[List[float]], str, int]:
        """Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to embed
            model_name: Optional model name to use
            
        Returns:
            Tuple of (embeddings, model_name, dimension)
        """
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        # Use specified model or default
        model = self._embedding_model
        if model_name and model_name != model.get_model_name():
            model = self._create_embedding_model(model_name)
        
        # Generate embeddings in batches
        embeddings = model.batch_embed(
            texts=texts,
            batch_size=settings.BATCH_SIZE
        )
        
        return embeddings, model.get_model_name(), model.get_dimension()
    
    def store_embeddings(
        self,
        texts: List[str],
        collection_name: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
        model_name: Optional[str] = None
    ) -> Tuple[List[str], str, int]:
        """Store embeddings in the vector database.
        
        Args:
            texts: List of texts to embed and store
            collection_name: Name of the collection
            metadata: Optional metadata for each text
            model_name: Optional model name to use
            
        Returns:
            Tuple of (ids, collection_name, count)
        """
        logger.info(f"Storing embeddings for {len(texts)} texts in collection '{collection_name}'")
        
        # Generate embeddings
        embeddings, model_name, dimension = self.generate_embeddings(texts, model_name)
        
        # Create collection if it doesn't exist
        if not self._vector_db.collection_exists(collection_name):
            self._vector_db.create_collection(collection_name, dimension)
        
        # Store embeddings
        ids = self._vector_db.add_vectors(
            collection_name=collection_name,
            vectors=embeddings,
            texts=texts,
            metadata=metadata
        )
        
        return ids, collection_name, len(ids)
    
    def query_similar(
        self,
        query_texts: List[str],
        collection_name: str,
        top_k: int = 5,
        model_name: Optional[str] = None
    ) -> Tuple[List[List[Dict[str, Any]]], str]:
        """Query for similar embeddings.
        
        Args:
            query_texts: List of query texts
            collection_name: Name of the collection
            top_k: Number of results to return
            model_name: Optional model name to use
            
        Returns:
            Tuple of (results, collection_name)
        """
        logger.info(f"Querying {len(query_texts)} texts in collection '{collection_name}'")
        
        # Check if collection exists
        if not self._vector_db.collection_exists(collection_name):
            raise ResourceNotFoundError(
                message=f"Collection '{collection_name}' does not exist",
                details={"collection_name": collection_name}
            )
        
        # Generate embeddings for query texts
        query_embeddings, _, _ = self.generate_embeddings(query_texts, model_name)
        
        # Query for similar embeddings
        results = self._vector_db.search(
            collection_name=collection_name,
            query_vectors=query_embeddings,
            top_k=top_k
        )
        
        return results, collection_name
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections.
        
        Returns:
            List of collection information
        """
        logger.info("Listing collections")
        return self._vector_db.list_collections()
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Deleting collection '{collection_name}'")
        return self._vector_db.delete_collection(collection_name)
    
    def get_health_info(self) -> Dict[str, Any]:
        """Get health information.
        
        Returns:
            Health information
        """
        return {
            "status": "healthy",
            "version": "0.1.0",
            "embedding_model": self._embedding_model.get_model_name(),
            "vector_db": settings.VECTOR_DB_TYPE
        }
