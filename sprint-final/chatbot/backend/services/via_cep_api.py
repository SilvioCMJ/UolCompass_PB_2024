from services.api import ApiClient


class ViaCepService:
    """
    Class to handle address-related operations using the ViaCEP API.
    """

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def get_cep(self, cep: str) -> dict:
        """Obtains the user's postal code information through the Via Cep API."""
        response = self.api_client.get(f"{cep}/json")
        if response.get("erro"):
            return None

        return response

    def format_cep_response(self, address_data: dict) -> str:
        """
        Formats the address data from a CEP (Brazilian postal code) query into
        a readable string.
        """

        street = address_data.get("logradouro", "N/A")
        neighborhood = address_data.get("bairro", "N/A")
        city = address_data.get("localidade", "N/A")
        state = address_data.get("uf", "N/A")
        region = address_data.get("regiao", "N/A")

        return street, neighborhood, city, state, region
