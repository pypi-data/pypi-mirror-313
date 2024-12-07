from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Literal, Union, Optional
from datetime import datetime


class MessageContact(BaseModel):
    """
    Schema for a message contact, representing either a contact ID or full contact details.

    Attributes:
        id (str): The unique identifier of the contact.
    """
    id: str = Field(
        ..., 
        description="The unique identifier of the contact.", 
        json_schema_extra={"example": "contact123"}
    )


class ContactDetails(BaseModel):
    """
    Schema for detailed contact information in a message.

    Attributes:
        name (str): The name of the contact.
        phone (str): The phone number of the contact.
        id (str): The unique identifier for the contact.
    """
    name: Optional[str] = Field(None, description="The name of the contact.", json_schema_extra={"example": "John Doe"})
    phone: Optional[str] = Field(None, description="The phone number of the contact.", json_schema_extra={"example": "+123456789"})
    id: str = Field(..., description="The unique ID of the contact.", json_schema_extra={"example": "contact-id-123"})
    
    
class CreateMessageRequest(BaseModel):
    """
    Schema for creating a new message.

    Attributes:
        to (Union[str, MessageContact]): Contact ID or full contact details of the recipient.
        content (str): Message content, with a maximum length of 160 characters.
        from_sender (str): Sender's phone number in E.164 format.
    """
    to: MessageContact = Field(
        ..., 
        description="Recipient's contact ID.", 
        json_schema_extra={"example": {"id": "contact123"}}
    )
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=160, 
        description="Message content, limited to 160 characters.",
        json_schema_extra={"example": "Hello, World!"}
    )
    from_sender: str = Field(
        ..., 
        alias="from", 
        description="Sender's phone number in E.164 format.",
        json_schema_extra={"example": "+0987654321"}
    )

    @field_validator("from_sender")
    def validate_phone_number(cls, value):
        if not value.startswith("+"):
            raise ValueError("Phone numbers must include the '+' prefix.")
        if not value[1:].isdigit():
            raise ValueError("Phone numbers must contain only digits after the '+' prefix.")
        return value


class Message(BaseModel):
    """
    Schema for a message resource.

    Attributes:
        id (str): Unique identifier for the message.
        from_sender (str): Sender's phone number.
        to (Union[ContactDetails, str]): Recipient details or just contact ID.
        content (str): Message content.
        status (str): Message status, one of 'queued', 'delivered', or 'failed'.
        created_at (datetime): Timestamp when the message was created.
        delivered_at (Optional[datetime]): Timestamp when the message was delivered.
    """
    id: str = Field(..., description="Unique identifier for the message.", json_schema_extra={"example": "msg123"})
    from_sender: str = Field(
        ..., 
        alias="from", 
        description="Sender's phone number.", 
        json_schema_extra={"example": "+0987654321"}
    )
    to: Union[ContactDetails, str] = Field(
        ..., 
        description="Recipient details or just contact ID."
    )
    content: str = Field(..., description="Message content.", json_schema_extra={"example": "Hello, World!"})
    status: Literal["queued", "delivered", "failed"] = Field(
        ..., 
        description="Message status.", 
        json_schema_extra={"example": "queued"}
    )
    created_at: datetime = Field(
        ..., 
        alias="createdAt", 
        description="Timestamp when the message was created.", 
        json_schema_extra={"example": "2024-12-06T03:01:37.416Z"}
    )
    delivered_at: Optional[datetime] = Field(
        None, 
        alias="deliveredAt", 
        description="Timestamp when the message was delivered.", 
        json_schema_extra={"example": "2024-12-06T03:01:37.416Z"}
    )

    @classmethod
    def validate_to_field(cls, value):
        """
        Custom validator for the 'to' field to normalize its structure.
        """
        if isinstance(value, str):
            # Treat the string as a contact ID and wrap it in a ContactDetails object
            return ContactDetails(id=value)
        elif isinstance(value, dict):
            # Parse it as a ContactDetails object
            return ContactDetails(**value)
        raise ValueError("'to' must be a valid contact ID (str) or ContactDetails object.")

    @classmethod
    def model_validate(cls, data):
        """
        Custom validation for the entire model to preprocess 'to'.
        """
        if "to" in data:
            data["to"] = cls.validate_to_field(data["to"])
        return super().model_validate(data)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class ListMessagesResponse(BaseModel):
    """
    Schema for listing messages with pagination support.

    Attributes:
        messages (List[Message]): List of message objects.
        page (int): Current page number.
        quantity_per_page (int): Number of messages per page.
    """
    messages: List[Message] = Field(..., description="List of message objects.")
    page: int = Field(..., description="Current page number.", json_schema_extra={"example": 1})
    quantity_per_page: int = Field(
        ..., 
        alias="quantityPerPage", 
        description="Number of messages per page.", 
        json_schema_extra={"example": 10}
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
