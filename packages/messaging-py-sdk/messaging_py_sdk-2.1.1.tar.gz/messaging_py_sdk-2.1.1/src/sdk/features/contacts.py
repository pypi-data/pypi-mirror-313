from typing import Dict, List
from httpx import HTTPStatusError

from ..client import ApiClient
from src.schemas.contacts import CreateContactRequest, Contact, ListContactsResponse
from src.core.validators import validate_request, validate_response
from src.core.exceptions import handle_exceptions, handle_404_error
from src.core.logger import logger


class Contacts:
    """
    Contacts SDK module for managing contacts via the API.

    Provides methods for creating, listing, retrieving, updating, and deleting contacts.
    """

    def __init__(self, client: ApiClient):
        """
        Initialize the Contacts module.

        Args:
            client (ApiClient): The shared API client instance.
        """
        self.client = client

    @validate_request(CreateContactRequest)
    @validate_response(Contact)
    @handle_exceptions
    def create_contact(self, payload: Dict) -> Contact:
        """
        Create a new contact in the system.

        Args:
            payload (dict): A dictionary containing 'name' and 'phone'.

        Returns:
            Contact: The created contact details.
        """
        logger.info(f"Creating contact with payload: {payload}")
        return self.client.request("POST", "/contacts", json=payload)


    @validate_response(ListContactsResponse)
    @handle_exceptions
    def list_contacts(self, page: int = 1, max: int = 10) -> ListContactsResponse:
        """
        List all contacts with pagination.

        Args:
            page (int): The page number to retrieve. Defaults to 1.
            max (int): The maximum number of contacts per page. Defaults to 10.

        Returns:
            ListContactsResponse: A paginated list of contacts.
        """
        params = {"pageIndex": page, "max": max}
        logger.info(f"Listing contacts with params: {params}")
        return self.client.request("GET", "/contacts", params=params)

    @validate_response(Contact)
    @handle_exceptions
    def get_contact(self, contact_id: str) -> Contact:
        """
        Retrieve a specific contact by ID.

        Args:
            contact_id (str): The unique ID of the contact.

        Returns:
            Contact: The retrieved contact details.
        """
        logger.info(f"Fetching contact with ID: {contact_id}")
        try:
            return self.client.request("GET", f"/contacts/{contact_id}")
        except HTTPStatusError as e:
            handle_404_error(e, contact_id, "Contact")

    @validate_request(CreateContactRequest)
    @validate_response(Contact)
    @handle_exceptions
    def update_contact(self, contact_id: str, payload: Dict) -> Contact:
        """
        Update the details of an existing contact.

        Args:
            contact_id (str): The unique ID of the contact.
            payload (dict): A dictionary containing 'name' and/or 'phone'.

        Returns:
            Contact: The updated contact details.
        """
        logger.info(f"Updating contact {contact_id} with payload: {payload}")
        try:
            return self.client.request("PATCH", f"/contacts/{contact_id}", json=payload)
        except HTTPStatusError as e:
            handle_404_error(e, contact_id, "Contact")

    @handle_exceptions
    def delete_contact(self, contact_id: str) -> None:
        """
        Delete a contact by ID.

        Args:
            contact_id (str): The unique ID of the contact.

        Returns:
            None
        """
        logger.info(f"Deleting contact with ID: {contact_id}")
        try:
            self.client.request("DELETE", f"/contacts/{contact_id}")
            logger.info(f"Successfully deleted contact with ID: {contact_id}")
        except HTTPStatusError as e:
            handle_404_error(e, contact_id, "Contact")
