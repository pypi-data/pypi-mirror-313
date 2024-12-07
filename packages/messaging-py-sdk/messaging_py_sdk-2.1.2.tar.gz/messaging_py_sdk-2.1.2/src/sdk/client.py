import requests
from typing import Any
from src.core.config import settings
from src.core.logger import logger
from src.core.requests import handle_request_errors
from src.core.exceptions import UnauthorizedError, NotFoundError, ServerError, ApiError, TransientError
from src.core.retry import retry


class ApiClient:
    """
    A base API client for handling HTTP requests with authentication, error handling, 
    and advanced retry logic for transient errors.
    """

    def __init__(self):
        """
        Initialize the API client with configuration and authentication details.
        """
        self.base_url = settings.BASE_URL
        self.api_key = settings.API_KEY


    def _handle_api_errors(self, response: requests.Response) -> None:
        """
        Handle API errors based on the HTTP status code.

        Args:
            response (requests.Response): The HTTP response object.

        Raises:
            UnauthorizedError: For 401 Unauthorized.
            NotFoundError: For 404 Not Found.
            TransientError: For retryable server errors like 502 or 503.
            ServerError: For other 500+ server errors.
            ApiError: Generic API error for unexpected status codes.
        """
        if response.status_code == 204:  # No Content
            logger.info("No content returned. Operation successful.")
            return
        elif response.status_code == 401:
            logger.error(f"Unauthorized: {response.text}")
            raise UnauthorizedError("Unauthorized. Check your API key.")
        elif response.status_code == 404:
            logger.error(f"Resource Not Found: {response.text}")
            raise NotFoundError("Resource not found.")
        elif response.status_code in (502, 503):
            logger.warning(f"Transient Error: {response.text}")
            raise TransientError("Transient server error. Please retry.", status_code=response.status_code)
        elif response.status_code >= 500:
            logger.error(f"Server Error: {response.text}")
            raise ServerError("Server error. Please try again later.")
        elif not response.ok:
            logger.error(f"Unhandled API Error: {response.status_code} - {response.text}")
            raise ApiError(f"Unhandled API Error: {response.status_code}: {response.text}")


    @retry(max_retries=3, backoff=2, retry_on=(502, 503))
    @handle_request_errors
    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Sends an HTTP request to the API server with retry and error handling.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint path (e.g., "/contacts").
            **kwargs: Additional arguments for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ApiError: For unexpected errors during the request.
        """
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        logger.info(f"Sending {method} request to {url} with headers {headers} and payload {kwargs}")
        response = requests.request(method, url, headers=headers, **kwargs)
        logger.info(f"Received response with status {response.status_code}")
        
        # Handle deletion api
        if response.status_code == 204:
            logger.info(f"Item successfully deleted.")
            return None

        # Handle API errors
        self._handle_api_errors(response)
        return response.json()
