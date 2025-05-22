"""
Logging utilities for the LLM service.
"""
import logging
import sys
from typing import Optional

from llm_service.config.settings import settings


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        name: Logger name. If None, returns the root logger.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = getattr(logging, settings.LOG_LEVEL)
    logger.setLevel(log_level)
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatters
    formatter = logging.Formatter(settings.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    
    return logger
