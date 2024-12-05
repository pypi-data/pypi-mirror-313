"""
Logging configuration.
"""
import logging
from typing import Any

def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Name for the logger
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler with formatting
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
