from src.core.logger import logger


class ApiError(Exception):
    """
    Base exception class for all API-related errors.

    Attributes:
        message (str): The error message describing the issue.
        status_code (int, optional): HTTP status code associated with the error (if applicable).
    """

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        if status_code:
            logger.error(f"[API Error] {status_code}: {message}")
        else:
            logger.error(f"[API Error]: {message}")

    def __str__(self):
        return f"{self.message} (HTTP {self.status_code})" if self.status_code else self.message


class UnauthorizedError(ApiError):
    """Exception raised for 401 Unauthorized errors."""

    def __init__(self, message: str = "Unauthorized access. Check your API key."):
        super().__init__(message, status_code=401)
        logger.warning("[UnauthorizedError] Ensure your API key is valid.")


class NotFoundError(ApiError):
    """Exception raised for 404 Not Found errors."""

    def __init__(self, message: str = "Requested resource not found."):
        super().__init__(message, status_code=404)
        logger.warning("[NotFoundError] Resource does not exist.")


class ServerError(ApiError):
    """Exception raised for 500+ Server Error responses."""

    def __init__(self, message: str = "Internal server error. Please try again later.", status_code: int = 500):
        super().__init__(message, status_code=status_code)
        logger.error("[ServerError] The server encountered an issue.")


class TransientError(ApiError):
    """Exception raised for transient server errors like 502 Bad Gateway or 503 Service Unavailable."""

    def __init__(self, message: str = "Transient server error. Please retry.", status_code: int = None):
        super().__init__(message, status_code=status_code)
        if status_code:
            logger.warning(f"[TransientError] {message} (HTTP {status_code})")
        else:
            logger.warning(f"[TransientError] {message}")
