"""
Base class for chunking strategies.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseChunkingStrategy(ABC):
    """Abstract base class for chunking strategies."""
    
    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the chunking strategy.
        
        Args:
            **kwargs: Strategy-specific parameters
        """
        pass
    
    @abstractmethod
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to include with each chunk
            
        Returns:
            List of chunks with text and metadata
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of the chunking strategy.
        
        Returns:
            Strategy name
        """
        pass
    
    @abstractmethod
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get the configuration of the chunking strategy.
        
        Returns:
            Strategy configuration
        """
        pass
