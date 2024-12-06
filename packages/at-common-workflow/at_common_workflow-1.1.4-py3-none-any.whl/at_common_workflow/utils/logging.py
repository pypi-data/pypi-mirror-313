import logging
from typing import Optional

def setup_logger(name: str = "workflow", level: Optional[int] = None) -> logging.Logger:
    """Set up and configure logger."""
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger