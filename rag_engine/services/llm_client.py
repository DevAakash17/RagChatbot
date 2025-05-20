"""
Client for interacting with the LLM Service.
"""
from typing import Dict, Any, Optional
import aiohttp
import json

from chatbot.rag_engine.core.config import settings
from chatbot.rag_engine.utils.errors import LLMServiceError, ServiceConnectionError
from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class LLMClient:
    """Client for the LLM Service."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the client.
        
        Args:
            base_url: Base URL for the LLM Service API
        """
        self.base_url = base_url or settings.LLM_SERVICE_URL
        logger.info(f"Initialized LLM Client with base URL: {self.base_url}")
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate text using the LLM.
        
        Args:
            prompt: Input prompt
            model: Optional model name to use
            options: Optional generation options
            
        Returns:
            Generated text and metadata
        """
        url = f"{self.base_url}/generate"
        
        payload = {
            "prompt": prompt,
            "model": model or settings.DEFAULT_LLM_MODEL,
            "options": options or settings.DEFAULT_LLM_OPTIONS
        }
        
        logger.info(f"Generating text with model: {payload['model']}")
        logger.debug(f"Prompt: {prompt}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    json=payload,
                    timeout=settings.TIMEOUT
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"LLM Service error: {error_text}")
                        raise LLMServiceError(
                            message=f"LLM Service returned status {response.status}",
                            details={"status": response.status, "response": error_text}
                        )
                    
                    response_data = await response.json()
                    
                    logger.debug(f"Generated text: {response_data['text'][:100]}...")
                    return response_data
        except aiohttp.ClientError as e:
            logger.error(f"Failed to connect to LLM Service: {str(e)}")
            raise ServiceConnectionError(
                message=f"Failed to connect to LLM Service: {str(e)}",
                details={"url": url}
            )
