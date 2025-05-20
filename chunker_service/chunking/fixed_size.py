"""
Fixed size chunking strategy.
"""
from typing import List, Dict, Any, Optional

from chatbot.chunker_service.core.logging import setup_logging
from chatbot.chunker_service.core.errors import ChunkingError
from chatbot.chunker_service.chunking.base import BaseChunkingStrategy


logger = setup_logging(__name__)


class FixedSizeChunkingStrategy(BaseChunkingStrategy):
    """Fixed size chunking strategy."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        **kwargs
    ):
        """Initialize the fixed size chunking strategy.
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
            **kwargs: Additional parameters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Validate parameters
        if self.chunk_size <= 0:
            raise ChunkingError("Chunk size must be positive")
        
        if self.chunk_overlap < 0:
            raise ChunkingError("Chunk overlap must be non-negative")
        
        if self.chunk_overlap >= self.chunk_size:
            raise ChunkingError("Chunk overlap must be less than chunk size")
        
        logger.info(f"Initialized FixedSizeChunkingStrategy with size={chunk_size}, overlap={chunk_overlap}")
    
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to include with each chunk
            
        Returns:
            List of chunks with text and metadata
        """
        if not text:
            logger.warning("Empty text provided for chunking")
            return []
        
        # Initialize result
        chunks = []
        
        # Initialize metadata
        base_metadata = metadata or {}
        
        # Calculate step size
        step_size = self.chunk_size - self.chunk_overlap
        
        # Chunk text
        for i in range(0, len(text), step_size):
            # Get chunk text
            chunk_text = text[i:i + self.chunk_size]
            
            # Skip empty chunks
            if not chunk_text.strip():
                continue
            
            # Create chunk metadata
            chunk_metadata = base_metadata.copy()
            chunk_metadata.update({
                "chunk_index": len(chunks),
                "chunk_start": i,
                "chunk_end": min(i + self.chunk_size, len(text)),
                "strategy": self.get_strategy_name(),
                "config": self.get_strategy_config()
            })
            
            # Add chunk
            chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
        
        logger.info(f"Created {len(chunks)} chunks from text of length {len(text)}")
        return chunks
    
    def get_strategy_name(self) -> str:
        """Get the name of the chunking strategy.
        
        Returns:
            Strategy name
        """
        return "fixed_size"
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get the configuration of the chunking strategy.
        
        Returns:
            Strategy configuration
        """
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
