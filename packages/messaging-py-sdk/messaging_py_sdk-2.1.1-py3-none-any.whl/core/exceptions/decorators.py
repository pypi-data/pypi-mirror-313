from httpx import HTTPStatusError
from src.core.logger import logger
from .resource import ContactNotFoundError, MessageNotFoundError
from .api import ApiError


def handle_exceptions(func):
    """
    Decorator to handle exceptions consistently across the SDK.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function with exception handling.

    Raises:
        ApiError: Reraises known API errors for logging and debugging.
        RuntimeError: Raises unexpected errors as runtime exceptions.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiError as api_error:
            logger.error(f"[ApiError]: {api_error}")
            raise
        except Exception as unexpected_error:
            logger.error(f"[Unhandled Exception]: {unexpected_error}")
            raise RuntimeError(f"An unexpected error occurred: {unexpected_error}")

    return wrapper


def handle_404_error(e: HTTPStatusError, resource_id: str, resource_type: str) -> None:
    """
    Handle 404 errors for specific resources.

    Args:
        e (HTTPStatusError): The HTTP exception.
        resource_id (str): The ID of the missing resource.
        resource_type (str): The type of the resource (e.g., "Contact", "Message").

    Raises:
        ResourceNotFoundError: A resource-specific not found error.
    """
    if e.response.status_code == 404:
        error_details = e.response.json()
        if resource_type == "Contact":
            raise ContactNotFoundError(
                resource_id,
                message=error_details.get("message", f"Contact with ID {resource_id} not found."),
            )
        elif resource_type == "Message":
            raise MessageNotFoundError(
                resource_id,
                message=error_details.get("message", f"Message with ID {resource_id} not found."),
            )
    raise  # Re-raise other HTTP errors
