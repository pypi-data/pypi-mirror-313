import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name: str = "MAS") -> logging.Logger:
    """Get logger instance with given name."""
    logger = logging.getLogger(name)
    return logger
