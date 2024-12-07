import json

from fastapi import FastAPI, HTTPException, Header, Request
from src.core.config import settings
from src.sdk.client import ApiClient
from src.schemas.webhook import WebhookPayload
from src.sdk.features.messages import Messages
from src.core.security import verify_signature
from src.core.logger import webhook_logger as logger
from src.schemas.errors import UnauthorizedError, BadRequestError, ServerError

# Initialize FastAPI app
app = FastAPI()

# SDK instance for validation
# Initialize ApiClient and Messages
api_client = ApiClient()
messages_sdk = Messages(client=api_client)


@app.post("/webhooks")
async def handle_webhook(
    payload: WebhookPayload,
    authorization: str = Header(...),
    request: Request = None,
):
    """
    Webhook endpoint to process incoming events.
    """
    try:
        # Extract raw request body
        raw_body = await request.body()

        # Validate signature using the SDK
        verify_signature(raw_body, authorization.removeprefix("Bearer "), settings.WEBHOOK_SECRET)

        # Log the received payload
        logger.info(f"Webhook received: {payload.model_dump()}")

        # Simulate event processing (printing is sufficient per task)
        print(f"Processed webhook payload: {payload.model_dump()}")

        return {"message": "Webhook processed successfully."}
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=BadRequestError(error=str(e)).model_dump()
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=401,
            detail=e.message
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=ServerError(message="An unexpected error occurred").model_dump()
        )
