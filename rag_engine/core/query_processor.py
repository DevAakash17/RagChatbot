"""
Query processor for the RAG Engine.
"""
from typing import Optional, Dict, Any
import re

from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class QueryProcessor:
    """Processes and optimizes user queries."""
    
    def __init__(self):
        """Initialize the query processor."""
        logger.info("Initialized QueryProcessor")
    
    def process_query(self, query: str) -> str:
        """Process and optimize a user query.
        
        Args:
            query: User query
            
        Returns:
            Processed query
        """
        logger.info(f"Processing query: {query}")
        
        # Remove extra whitespace
        processed_query = re.sub(r'\s+', ' ', query).strip()
        
        # Convert to lowercase
        processed_query = processed_query.lower()
        
        # Remove special characters
        processed_query = re.sub(r'[^\w\s]', '', processed_query)
        
        logger.info(f"Processed query: {processed_query}")
        return processed_query
    
    def extract_metadata(self, query: str) -> Dict[str, Any]:
        """Extract metadata from a query.
        
        Args:
            query: User query
            
        Returns:
            Extracted metadata
        """
        # This is a placeholder for more advanced metadata extraction
        # In a real implementation, this could extract entities, intents, etc.
        metadata = {
            "length": len(query),
            "word_count": len(query.split())
        }
        
        logger.debug(f"Extracted metadata: {metadata}")
        return metadata
