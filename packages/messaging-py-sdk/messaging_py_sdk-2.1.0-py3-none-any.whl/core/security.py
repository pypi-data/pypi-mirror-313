import hmac
import json
import hashlib

from functools import wraps
from .logger import logger
from src.schemas.errors import UnauthorizedError


def generate_signature(payload: dict, secret: str) -> str:
    """
    Generate HMAC signature for a given payload.

    Args:
        payload (dict): The payload to sign.
        secret (str): The secret key.

    Returns:
        str: Hexadecimal HMAC signature.
    """
    try:
        # Serialize payload to JSON with stable formatting
        message = json.dumps(payload, separators=(",", ":")).encode("utf-8")  # Convert to bytes
        hmac_instance = hmac.new(secret.encode("utf-8"), message, hashlib.sha256)
        return hmac_instance.hexdigest()
    except Exception as e:
        raise ValueError(f"Error generating signature: {str(e)}")


def verify_signature(message: bytes, signature: str, secret: str):
    """
    Validate the HMAC signature of incoming webhooks.

    Args:
        message (bytes): Raw request body in bytes.
        signature (str): Authorization header signature.
        secret (str): Webhook secret.

    Raises:
        UnauthorizedError: If the signature is invalid.
    """
    logger.info("Validating HMAC signature.")
    try:
        # Create HMAC using secret and SHA256
        hmac_instance = hmac.new(secret.encode("utf-8"), message, hashlib.sha256)
        expected_signature = hmac_instance.hexdigest()

        # Validate the signature
        if not hmac.compare_digest(expected_signature, signature):
            logger.error("Invalid HMAC signature.")
            raise UnauthorizedError(
                message="Unauthorized: Signature validation failed."
            )

        logger.info("HMAC signature validated successfully.")
        return True

    except Exception as e:
        logger.error(f"Error validating signature: {str(e)}")
        raise
