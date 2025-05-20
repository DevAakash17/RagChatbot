"""
Sentence Transformers implementation of the embedding model.
"""
import torch
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseEmbeddingModel
from ..core.errors import EmbeddingModelError


class SentenceTransformerModel(BaseEmbeddingModel):
    """Sentence Transformers implementation of the embedding model."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", **kwargs):
        """Initialize the Sentence Transformers model.
        
        Args:
            model_name: Name of the model to use
            **kwargs: Additional model parameters
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading Sentence Transformers model: {model_name}")
            self.model_name = model_name
            self.model = SentenceTransformer(model_name, **kwargs)
            
            # Set device if specified
            device = kwargs.get('device')
            if device:
                self.model.to(device)
                
            logger.info(f"Model loaded successfully with dimension: {self.get_dimension()}")
        except Exception as e:
            error_msg = f"Failed to initialize Sentence Transformers model: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg, details={"model_name": model_name})
    
    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to embed
            **kwargs: Additional embedding parameters
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Get embeddings
            embeddings = self.model.encode(
                texts,
                convert_to_tensor=False,
                normalize_embeddings=kwargs.get('normalize', True),
                show_progress_bar=kwargs.get('show_progress', False)
            )
            
            # Convert to list of lists
            return embeddings.tolist() if not isinstance(embeddings, list) else embeddings
        except Exception as e:
            error_msg = f"Failed to generate embeddings: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg)
    
    def get_dimension(self) -> int:
        """Get the dimension of the embeddings.
        
        Returns:
            Dimension of the embeddings
        """
        return self.model.get_sentence_embedding_dimension()
    
    def get_model_name(self) -> str:
        """Get the name of the model.
        
        Returns:
            Name of the model
        """
        return self.model_name
    
    def batch_embed(self, texts: List[str], batch_size: int = 32, **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Size of each batch
            **kwargs: Additional embedding parameters
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Get embeddings in batches
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_tensor=False,
                normalize_embeddings=kwargs.get('normalize', True),
                show_progress_bar=kwargs.get('show_progress', False)
            )
            
            # Convert to list of lists
            return embeddings.tolist() if not isinstance(embeddings, list) else embeddings
        except Exception as e:
            error_msg = f"Failed to generate batch embeddings: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg, details={"batch_size": batch_size})
