import requests

from functools import wraps
from .logger import logger

def handle_request_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTPError: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {e}")
            raise
    return wrapper
