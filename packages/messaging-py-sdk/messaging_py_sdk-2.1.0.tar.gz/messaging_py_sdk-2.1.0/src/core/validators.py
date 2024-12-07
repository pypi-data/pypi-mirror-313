from pydantic import ValidationError
from functools import wraps
from typing import Any, Callable
from .logger import logger


def validate_request(model: Any):
    """
    Decorator to validate request payloads using a Pydantic model.
    Logs detailed errors for invalid inputs and halts execution.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "payload" in kwargs:
                try:
                    logger.debug("Entering validate_request decorator.")
                    logger.info(f"Validating request payload: {kwargs['payload']}")
                    model(**kwargs["payload"])  # Validate the payload
                    logger.debug("Exiting validate_request decorator.")
                except ValidationError as e:
                    logger.error(f"Request Validation Error: {e.json()}")
                    for error in e.errors():
                        logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                    raise ValueError("Invalid payload")  # Halt execution here
            else:
                logger.warning("No payload provided for validation.")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_response(model: Any):
    """
    Decorator to validate API responses using a Pydantic model.
    Logs detailed errors for invalid responses.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Entering validate_response decorator.")
            response = func(*args, **kwargs)
            try:
                model(**response)  # Validate the response
                logger.debug("Exiting validate_response decorator.")
                return response
            except ValidationError as e:
                logger.error(f"Response Validation Error: {e.json()}")
                for error in e.errors():
                    logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                raise ValueError(f"Invalid response: {e}")
        return wrapper
    return decorator
