"""
Response generator for the RAG Engine.
"""
from typing import Dict, Any, Optional

from chatbot.rag_engine.core.config import settings
from chatbot.rag_engine.services.llm_client import LLMClient
from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class ResponseGenerator:
    """Generates responses using the LLM."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize the response generator.
        
        Args:
            llm_client: Optional LLM client
        """
        self.llm_client = llm_client or LLMClient()
        logger.info("Initialized ResponseGenerator")
    
    async def generate_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a response for a prompt.
        
        Args:
            prompt: Input prompt
            model: Optional model name to use
            options: Optional generation options
            
        Returns:
            Generated response and metadata
        """
        logger.info(f"Generating response with model: {model or settings.DEFAULT_LLM_MODEL}")
        
        # Generate text using the LLM service
        response = await self.llm_client.generate_text(
            prompt=prompt,
            model=model,
            options=options
        )
        
        logger.info("Response generated successfully")
        return response
