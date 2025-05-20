"""
Base class for embedding models.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseEmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    def __init__(self, model_name: str, **kwargs):
        """Initialize the embedding model.
        
        Args:
            model_name: Name of the embedding model
            **kwargs: Additional model-specific parameters
        """
        pass
    
    @abstractmethod
    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to embed
            **kwargs: Additional embedding parameters
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of the embeddings.
        
        Returns:
            Dimension of the embeddings
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the model.
        
        Returns:
            Name of the model
        """
        pass
    
    @abstractmethod
    def batch_embed(self, texts: List[str], batch_size: int, **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Size of each batch
            **kwargs: Additional embedding parameters
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        pass
