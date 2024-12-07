from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class WebhookPayload(BaseModel):
    """
    Schema for webhook payloads received from the API server.
    Represents the MessageDeliveryEvent schema from the OpenAPI specification.

    Attributes:
        id (str): Unique identifier for the message.
        status (str): The status of the message, one of 'queued', 'delivered', or 'failed'.
        delivered_at (datetime, optional): Timestamp when the message was delivered, if applicable.
    """
    id: str = Field(
        ..., 
        description="Unique identifier for the message.", 
        json_schema_extra={"example": "msg123"}
    )
    status: Literal["queued", "delivered", "failed"] = Field(
        ..., 
        description="The status of the message.", 
        json_schema_extra={"example": "delivered"}
    )
    delivered_at: Optional[datetime] = Field(
        None, 
        alias="deliveredAt", 
        description="Timestamp when the message was delivered, if applicable.",
        json_schema_extra={"example": "2024-12-01T12:00:00Z"}
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
