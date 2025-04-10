import os

from services.api import ApiClient


class AmazonServices:
    """Class to handle institution-related operations."""

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def create_institution(self, institution_data: dict) -> dict:
        """Creates a new institution by sending data to the API."""
        return self.api_client.post(os.getenv("POST_INSTITUTIONS"), institution_data)

    def post_bedrock(self, data: dict) -> dict:
        """Send a prompt to AWS Bedrock and receive a response."""
        return self.api_client.post(os.getenv("POST_BEDROCK"), data)
