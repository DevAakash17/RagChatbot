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

        # Add additional parameters for model loading
        model_params = {
            'cache_folder': settings.MODEL_CACHE_DIR,
        }

        # If force download is enabled, add a unique cache folder to bypass cache
        if settings.FORCE_MODEL_DOWNLOAD:
            import tempfile
            import os
            import uuid
            # Create a unique temporary directory for this download
            temp_dir = os.path.join(tempfile.gettempdir(), f"st_model_{uuid.uuid4().hex}")
            os.makedirs(temp_dir, exist_ok=True)
            model_params['cache_folder'] = temp_dir
            logger.info(f"Forcing model download to temporary directory: {temp_dir}")

        # Currently only supporting Sentence Transformers
        model = SentenceTransformerModel(model_name=model_name, **model_params)

        # Verify the model dimension matches what we expect
        actual_dim = model.get_dimension()
        expected_dim = settings.EMBEDDING_DIMENSION

        if actual_dim != expected_dim:
            logger.warning(f"Model dimension mismatch: expected {expected_dim}, got {actual_dim}")
            if 'bge-large' in model_name and actual_dim != 1024:
                logger.error(f"The BGE large model should have 1024 dimensions but has {actual_dim}. This indicates a loading problem.")

        return model

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
        """Query for similar embeddings with improved processing.

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

        # Get collection info to check dimension
        collection_info = self._vector_db.get_collection_info(collection_name)
        collection_dimension = collection_info.get("dimension", 0)

        # Use the specified model or default to BAAI/bge-small-en-v1.5
        effective_model_name = model_name or "BAAI/bge-small-en-v1.5"

        # Log a warning if dimensions don't match
        if collection_dimension > 0 and collection_dimension != 384:
            logger.warning(f"Collection '{collection_name}' has dimension {collection_dimension} which doesn't match the expected dimension 384")
            logger.warning(f"This may cause errors. Consider reindexing the collection with the BAAI/bge-small-en-v1.5 model.")

        # Preprocess and expand queries
        processed_queries = []
        original_queries = []
        for query in query_texts:
            # Store original query for reranking
            original_queries.append(query)

            # Simple preprocessing - remove extra whitespace, lowercase
            clean_query = " ".join(query.lower().split())
            processed_queries.append(clean_query)

            # Add query expansion if needed
            # processed_queries.extend(self._expand_query(clean_query))

        # Generate embeddings for processed query texts
        query_embeddings, _, _ = self.generate_embeddings(processed_queries, effective_model_name)

        # Query for similar embeddings
        results = self._vector_db.search(
            collection_name=collection_name,
            query_vectors=query_embeddings,
            top_k=top_k * 2  # Get more results for reranking
        )

        # Rerank results
        reranked_results = []
        for i, result_list in enumerate(results):
            # Use original query for reranking
            reranked = self._rerank_results(original_queries[i], result_list, top_k)
            reranked_results.append(reranked)

        return reranked_results, collection_name

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

    def _rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Rerank results to improve relevance.

        Args:
            query: Original query text
            results: Initial search results
            top_k: Number of results to return

        Returns:
            Reranked results
        """
        # Simple reranking based on exact matches and metadata
        for result in results:
            # Initialize boost
            boost = 0.0

            # Boost for exact matches
            query_terms = query.lower().split()
            for term in query_terms:
                if term in result["text"].lower():
                    boost += 0.05  # Small boost per matching term

            # Boost based on metadata (if available)
            metadata = result.get("metadata", {})
            if metadata:
                # Example: boost documents with specific metadata
                if "document_type" in metadata:
                    doc_type = metadata.get("document_type", "").lower()
                    if "policy" in doc_type:
                        boost += 0.15  # Higher boost for policy documents
                    elif "summary" in doc_type:
                        boost += 0.1  # Medium boost for summaries

                # Example: boost documents with more complete metadata
                metadata_completeness = len(metadata) / 10.0  # Normalize by assuming 10 fields is complete
                boost += min(0.1, metadata_completeness * 0.1)  # Max 0.1 boost for metadata completeness

            # Apply the boost (capped at 1.0)
            result["score"] = min(1.0, result["score"] + boost)

        # Sort by updated score
        reranked = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

        return reranked

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
