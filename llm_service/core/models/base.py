"""
Base model interface for LLM models.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMModel(ABC):
    """Base class for LLM models."""
    
    def __init__(self, model_name: str, config: Dict[str, Any]):
        """
        Initialize the model.
        
        Args:
            model_name: Name of the model.
            config: Model configuration.
        """
        self.model_name = model_name
        self.config = config
    
    @abstractmethod
    async def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate text based on the prompt.
        
        Args:
            prompt: Input prompt.
            options: Additional options for generation.
            
        Returns:
            Generated text and metadata.
        """
        pass
