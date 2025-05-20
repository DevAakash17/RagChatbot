"""
Logging configuration for the Embedding Service.
"""
import sys
import logging
from pathlib import Path
from loguru import logger

from .config import settings


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages toward Loguru.
    
    This handler intercepts all standard logging messages and redirects them
    to Loguru for consistent formatting and handling.
    """
    
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    """Configure logging for the application."""
    # Remove default handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_LEVEL)
    
    # Remove all Loguru handlers
    logger.configure(handlers=[])
    
    # Configure Loguru
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # Console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
    )
    
    # File handler (if configured)
    if settings.LOG_FILE:
        log_file = Path(settings.LOG_FILE)
        logger.add(
            log_file,
            format=log_format,
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            compression="zip",
            retention="1 month",
        )
    
    # Intercept standard library logging
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    
    return logger
