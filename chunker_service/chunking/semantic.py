"""
Semantic chunking strategy.
"""
import re
from typing import List, Dict, Any, Optional

from chunker_service.core.logging import setup_logging
from chunker_service.core.errors import ChunkingError
from chunker_service.chunking.base import BaseChunkingStrategy


logger = setup_logging(__name__)


class SemanticChunkingStrategy(BaseChunkingStrategy):
    """Semantic chunking strategy."""
    
    def __init__(
        self,
        max_chunk_size: int = 1500,
        min_chunk_size: int = 500,
        **kwargs
    ):
        """Initialize the semantic chunking strategy.
        
        Args:
            max_chunk_size: Maximum size of each chunk in characters
            min_chunk_size: Minimum size of each chunk in characters
            **kwargs: Additional parameters
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        
        # Validate parameters
        if self.max_chunk_size <= 0:
            raise ChunkingError("Maximum chunk size must be positive")
        
        if self.min_chunk_size <= 0:
            raise ChunkingError("Minimum chunk size must be positive")
        
        if self.min_chunk_size > self.max_chunk_size:
            raise ChunkingError("Minimum chunk size must be less than or equal to maximum chunk size")
        
        logger.info(f"Initialized SemanticChunkingStrategy with max_size={max_chunk_size}, min_size={min_chunk_size}")
    
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces based on semantic boundaries.
        
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
        
        # Split text into paragraphs
        paragraphs = self._split_into_paragraphs(text)
        
        # Combine paragraphs into chunks
        current_chunk = ""
        current_start = 0
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed max_chunk_size and we already have content,
            # finalize the current chunk
            if current_chunk and len(current_chunk) + len(paragraph) > self.max_chunk_size:
                # Create chunk metadata
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    "chunk_index": len(chunks),
                    "chunk_start": current_start,
                    "chunk_end": current_start + len(current_chunk),
                    "strategy": self.get_strategy_name(),
                    "config": self.get_strategy_config()
                })
                
                # Add chunk
                chunks.append({
                    "text": current_chunk,
                    "metadata": chunk_metadata
                })
                
                # Reset current chunk
                current_chunk = ""
            
            # If paragraph itself exceeds max_chunk_size, split it further
            if len(paragraph) > self.max_chunk_size:
                # If we have a current chunk, finalize it first
                if current_chunk:
                    # Create chunk metadata
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        "chunk_index": len(chunks),
                        "chunk_start": current_start,
                        "chunk_end": current_start + len(current_chunk),
                        "strategy": self.get_strategy_name(),
                        "config": self.get_strategy_config()
                    })
                    
                    # Add chunk
                    chunks.append({
                        "text": current_chunk,
                        "metadata": chunk_metadata
                    })
                    
                    # Reset current chunk
                    current_chunk = ""
                
                # Split paragraph into sentences
                sentences = self._split_into_sentences(paragraph)
                
                # Combine sentences into chunks
                sentence_chunk = ""
                sentence_start = current_start + len(current_chunk)
                
                for sentence in sentences:
                    # If adding this sentence would exceed max_chunk_size and we already have content,
                    # finalize the current sentence chunk
                    if sentence_chunk and len(sentence_chunk) + len(sentence) > self.max_chunk_size:
                        # Create chunk metadata
                        chunk_metadata = base_metadata.copy()
                        chunk_metadata.update({
                            "chunk_index": len(chunks),
                            "chunk_start": sentence_start,
                            "chunk_end": sentence_start + len(sentence_chunk),
                            "strategy": self.get_strategy_name(),
                            "config": self.get_strategy_config()
                        })
                        
                        # Add chunk
                        chunks.append({
                            "text": sentence_chunk,
                            "metadata": chunk_metadata
                        })
                        
                        # Reset sentence chunk
                        sentence_chunk = ""
                        sentence_start = current_start + len(current_chunk)
                    
                    # Add sentence to sentence chunk
                    sentence_chunk += sentence
                
                # Add any remaining sentence chunk
                if sentence_chunk:
                    # Create chunk metadata
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        "chunk_index": len(chunks),
                        "chunk_start": sentence_start,
                        "chunk_end": sentence_start + len(sentence_chunk),
                        "strategy": self.get_strategy_name(),
                        "config": self.get_strategy_config()
                    })
                    
                    # Add chunk
                    chunks.append({
                        "text": sentence_chunk,
                        "metadata": chunk_metadata
                    })
            else:
                # Add paragraph to current chunk
                if not current_chunk:
                    current_start = text.find(paragraph)
                
                current_chunk += paragraph
        
        # Add any remaining content
        if current_chunk:
            # Create chunk metadata
            chunk_metadata = base_metadata.copy()
            chunk_metadata.update({
                "chunk_index": len(chunks),
                "chunk_start": current_start,
                "chunk_end": current_start + len(current_chunk),
                "strategy": self.get_strategy_name(),
                "config": self.get_strategy_config()
            })
            
            # Add chunk
            chunks.append({
                "text": current_chunk,
                "metadata": chunk_metadata
            })
        
        logger.info(f"Created {len(chunks)} chunks from text of length {len(text)}")
        return chunks
    
    def get_strategy_name(self) -> str:
        """Get the name of the chunking strategy.
        
        Returns:
            Strategy name
        """
        return "semantic"
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get the configuration of the chunking strategy.
        
        Returns:
            Strategy configuration
        """
        return {
            "max_chunk_size": self.max_chunk_size,
            "min_chunk_size": self.min_chunk_size
        }
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs.
        
        Args:
            text: Text to split
            
        Returns:
            List of paragraphs
        """
        # Split by double newlines (common paragraph separator)
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter out empty paragraphs
        paragraphs = [p for p in paragraphs if p.strip()]
        
        # Ensure paragraphs end with newlines
        paragraphs = [p if p.endswith('\n') else p + '\n' for p in paragraphs]
        
        return paragraphs
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting - this could be improved with NLP libraries
        # for more accurate sentence boundary detection
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        sentences = [s for s in sentences if s.strip()]
        
        # Ensure sentences end with spaces
        sentences = [s if s.endswith(' ') else s + ' ' for s in sentences]
        
        return sentences
