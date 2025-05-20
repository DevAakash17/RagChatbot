"""
Core LLM service implementation.
"""
from typing import Dict, Any, Optional, Type

from chatbot.llm_service.config.settings import settings
from chatbot.llm_service.core.models.base import BaseLLMModel
from chatbot.llm_service.core.models.gemini import GeminiModel
from chatbot.llm_service.utils.errors import ModelNotFoundError
from chatbot.llm_service.utils.logging import setup_logging


logger = setup_logging(__name__)


class LLMService:
    """Service for generating text using LLM models."""
    
    # Registry of available model implementations
    _model_registry: Dict[str, Type[BaseLLMModel]] = {
        "gemini-2.0-flash": GeminiModel,
    }
    
    # Cache of initialized model instances
    _model_instances: Dict[str, BaseLLMModel] = {}
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseLLMModel:
        """
        Get a model instance by name.
        
        Args:
            model_name: Name of the model.
            
        Returns:
            Model instance.
            
        Raises:
            ModelNotFoundError: If the model is not found.
        """
        # Check if model is already initialized
        if model_name in cls._model_instances:
            return cls._model_instances[model_name]
        
        # Check if model is in registry
        if model_name not in cls._model_registry:
            logger.error(f"Model '{model_name}' not found in registry")
            raise ModelNotFoundError(model_name)
        
        # Check if model config exists
        if model_name not in settings.MODEL_CONFIGS:
            logger.error(f"Model '{model_name}' not found in configuration")
            raise ModelNotFoundError(model_name)
        
        # Get model config
        model_config = settings.MODEL_CONFIGS[model_name]
        
        # Add API key to config
        if model_name.startswith("gemini"):
            model_config["api_key"] = settings.GEMINI_API_KEY
        
        # Initialize model
        model_class = cls._model_registry[model_name]
        model_instance = model_class(model_name, model_config)
        
        # Cache model instance
        cls._model_instances[model_name] = model_instance
        
        logger.info(f"Initialized model: {model_name}")
        return model_instance
    
    @classmethod
    async def generate_text(
        cls, 
        prompt: str, 
        model_name: str = "gemini-2.0-flash", 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate text based on the prompt.
        
        Args:
            prompt: Input prompt.
            model_name: Name of the model to use.
            options: Additional options for generation.
            
        Returns:
            Generated text and metadata.
        """
        logger.info(f"Generating text with model: {model_name}")
        model = cls.get_model(model_name)
        return await model.generate(prompt, options)
    
    @classmethod
    def register_model(cls, model_name: str, model_class: Type[BaseLLMModel]) -> None:
        """
        Register a new model implementation.
        
        Args:
            model_name: Name of the model.
            model_class: Model implementation class.
        """
        cls._model_registry[model_name] = model_class
        logger.info(f"Registered new model: {model_name}")


    @staticmethod
    def get_health_info() -> Dict[str, Any]:
        """Get health information.

        Returns:
            Health information
        """
        return {
            "status": "healthy",
            "version": "0.1.0"
        }
