import requests
import os
from requests.exceptions import RequestException


def download_media_file(media_url: str) -> bytes:
    """Downloads the media file from the provided URL."""
    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")

    try:
        response = requests.get(media_url, auth=(account_sid, auth_token))
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError(
                f"Request failed with status code {response.status_code}. "
                f"Content-Type: {response.headers.get('Content-Type')}. "
                f"Response content: {response.text}"
            )
    except RequestException as e:
        raise Exception(
            f"Failed to download media from {media_url}. Error: {str(e)}"
        ) from e
