"""Module for logging."""
import logging
from typing import Optional


def get_module_logger(module_name: str, format_str: Optional[str] = None):
    """Get a module logger from builtin logging library. To use this, do "logger = get_module_logger(__name__)"
    """
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    if format_str is not None:
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
