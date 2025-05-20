"""
Logging utilities for the RAG Engine.
"""
import logging
import sys
from typing import Optional

from chatbot.rag_engine.core.config import settings


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """Set up logging for the application.
    
    Args:
        name: Logger name (optional)
        
    Returns:
        Configured logger
    """
    # Get logger
    logger = logging.getLogger(name or "rag_engine")
    
    # Set log level
    log_level = getattr(logging, settings.LOG_LEVEL)
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if settings.LOG_FILE:
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
