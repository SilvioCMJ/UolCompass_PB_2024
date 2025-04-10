import requests


class ApiClient:
    """Class to handle API connections."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def _send_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Helper method to send HTTP requests."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method, url, json=data)

            if response.status_code not in [200, 201]:
                raise ValueError(f"Unexpected status code: {response.status_code}.")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise e

    def post(self, endpoint: str, data: dict) -> dict:
        """Sends a POST request to the specified endpoint."""
        return self._send_request("POST", endpoint, data)

    def get(self, endpoint: str) -> dict:
        """Sends a GET request to the specified endpoint."""
        return self._send_request("GET", endpoint)
