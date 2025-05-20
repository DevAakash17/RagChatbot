"""
Chunking module for the Chunker Service.
"""
from typing import Dict, Any, Optional

from chatbot.chunker_service.core.config import settings
from chatbot.chunker_service.core.errors import ChunkingError
from chatbot.chunker_service.core.logging import setup_logging
from chatbot.chunker_service.chunking.base import BaseChunkingStrategy
from chatbot.chunker_service.chunking.fixed_size import FixedSizeChunkingStrategy
from chatbot.chunker_service.chunking.semantic import SemanticChunkingStrategy


logger = setup_logging(__name__)


def get_chunking_strategy(strategy_type: Optional[str] = None, **kwargs) -> BaseChunkingStrategy:
    """Get a chunking strategy.
    
    Args:
        strategy_type: Type of chunking strategy
        **kwargs: Additional parameters
        
    Returns:
        Chunking strategy instance
    """
    # Use specified strategy type or default
    strategy_type = strategy_type or settings.DEFAULT_CHUNKING_STRATEGY
    
    logger.info(f"Creating chunking strategy: {strategy_type}")
    
    if strategy_type.lower() == "fixed_size":
        return FixedSizeChunkingStrategy(
            chunk_size=kwargs.get("chunk_size", settings.DEFAULT_CHUNK_SIZE),
            chunk_overlap=kwargs.get("chunk_overlap", settings.DEFAULT_CHUNK_OVERLAP)
        )
    elif strategy_type.lower() == "semantic":
        return SemanticChunkingStrategy(
            max_chunk_size=kwargs.get("max_chunk_size", settings.DEFAULT_CHUNK_SIZE * 1.5),
            min_chunk_size=kwargs.get("min_chunk_size", settings.DEFAULT_CHUNK_SIZE * 0.5)
        )
    else:
        raise ChunkingError(f"Unsupported chunking strategy: {strategy_type}")
