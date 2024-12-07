import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Central logger
def get_logger(context="sdk"):
    """
    Get a logger with a specific context.

    Args:
        context (str): Context for the logger (e.g., 'sdk', 'webhooks').

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(f"logger.{context}")
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    console_handler.setFormatter(console_format)

    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.WARNING)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler.setFormatter(file_format)

    # Add handlers if not already added
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Create loggers for SDK and Webhook
logger = get_logger("sdk")
webhook_logger = get_logger("webhooks")
