import time
from functools import wraps
from .logger import logger
from .exceptions import TransientError


def retry(max_retries: int = 3, backoff: int = 2, retry_on: tuple = (502, 503)):
    """
    Retry decorator for handling transient errors.

    Args:
        max_retries (int): Maximum number of retries.
        backoff (int): Backoff time in seconds between retries.
        retry_on (tuple): HTTP status codes to retry on.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if e.status_code in retry_on:
                        logger.warning(f"Retrying due to {e} (attempt {retries + 1}/{max_retries})...")
                        retries += 1
                        time.sleep(backoff)
                    else:
                        raise
            raise RuntimeError(f"Failed after {max_retries} retries.")
        return wrapper
    return decorator
