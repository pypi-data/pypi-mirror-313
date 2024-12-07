from pydantic import BaseModel, Field


class BadRequestError(BaseModel):
    """
    Schema for Bad Request Error (400).
    """
    error: str = Field(
        ...,
        description="Detailed error message.",
        json_schema_extra={"example": "Invalid input data."}
    )


class UnauthorizedError(Exception):
    """
    Custom exception for unauthorized access.
    """
    def __init__(self, message="Unauthorized access"):
        super().__init__(message)
        self.message = message


class UnauthorizedErrorSchema(BaseModel):
    """
    Schema for Unauthorized Error (401).
    """
    message: str = Field(
        ...,
        description="Authorization error message.",
        json_schema_extra={"example": "Unauthorized access."}
    )


class ServerError(BaseModel):
    """
    Schema for Internal Server Error (500).
    """
    message: str = Field(
        ...,
        description="Server error message.",
        json_schema_extra={"example": "An unexpected error occurred."}
    )


class MessageNotFoundError(BaseModel):
    """
    Schema for Message Not Found Error (404) specific to messages.
    """
    id: str = Field(
        ...,
        description="The ID of the missing message.",
        json_schema_extra={"example": "msg123"}
    )
    message: str = Field(
        ...,
        description="Error message.",
        json_schema_extra={"example": "Message not found."}
    )


class ContactNotFoundError(BaseModel):
    """
    Schema for Contact Not Found Error (404) specific to contacts.
    """
    id: str = Field(
        ...,
        description="The ID of the missing contact.",
        json_schema_extra={"example": "contact456"}
    )
    message: str = Field(
        ...,
        description="Error message.",
        json_schema_extra={"example": "Contact not found."}
    )
