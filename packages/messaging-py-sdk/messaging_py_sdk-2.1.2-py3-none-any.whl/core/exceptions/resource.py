from src.core.exceptions.api import ApiError


class ResourceNotFoundError(ApiError):
    """
    Base exception for resource not found errors.

    Attributes:
        resource_id (str): The ID of the missing resource.
        resource_name (str): The name of the resource type (e.g., "Contact", "Message").
    """

    def __init__(self, id: str, resource_name: str, message: str = None):
        message = message or f"{resource_name} with ID {id} not found."
        super().__init__(message, status_code=404)
        self.id = id
        self.resource_name = resource_name


class ContactNotFoundError(ResourceNotFoundError):
    """Exception for Contact not found."""
    def __init__(self, id: str, message: str = "Contact not found."):
        super().__init__(id=id, resource_name="Contact", message=message)


class MessageNotFoundError(ResourceNotFoundError):
    """Exception for Message not found."""
    def __init__(self, id: str, message: str = "Message not found."):
        super().__init__(id=id, resource_name="Message", message=message)
