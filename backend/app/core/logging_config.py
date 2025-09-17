import logging
import sys
from typing import Dict, Any

def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the ConvoCanvas application
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    # Set specific logger levels
    loggers = {
        "uvicorn.access": logging.WARNING,
        "fastapi": logging.INFO,
        "app": logging.INFO,
    }

    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name"""
    return logging.getLogger(name)