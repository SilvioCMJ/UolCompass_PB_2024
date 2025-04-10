import os

from services.api import ApiClient
from services.aws import AmazonServices
from utils.responses import LexResponses
from utils.slots import check_slot_filling, get_slot_value
from services.polly import generate_audio_as_bytes
from services.s3 import upload_file_to_s3


class RegisterIntent:
    """
    Class responsible for handling events related to the RegisterIntent intent.
    """

    validation_rules = {
        "CNPJ": r"^\d{14}$",
        "InstitutionName": r"^[\w\s.,&-]{2,}$",
        "InstitutionEmail": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "InstitutionPhone": r"^\d{11}$",
        "InstitutionAddressNumber": r"^\d+$",
        "InstitutionSite": r"^(https?://)?(www\.)?([a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+)(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=%]*)?$",
        "InstitutionCep": r"^\d{8}$",
        "InstitutionDescription": r"^[A-Za-z0-9\w\s.,&-]{10,150}$",
    }

    def __init__(self, event: dict) -> None:
        self.event = event
        self.bucket_name = os.getenv("BUCKET_NAME")

    def process_dialog_hook(self) -> LexResponses:
        """
        Responsible for processing the DialogCodeHook step of the RegisterIntent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        return check_slot_filling(slots, self.event, self.__class__.validation_rules)

    def process_full_fillment(self) -> LexResponses:
        """
        Responsible for processing the FulfillmentCodeHook step of the RegisterIntent.
        """
        print(f"Evento no fulfillment: {self.event}")
        slots = self.event["sessionState"]["intent"]["slots"]

        institution_data = self.generate_institution_data(slots)

        api_client = ApiClient(os.getenv("BASE_URL"))
        amazon_service = AmazonServices(api_client)

        try:
            amazon_service.create_institution(institution_data)
            response_message = (
                "Cadastro da instituição realizado com sucesso! "
                "Ele estará disponível assim que aprovado. "
                "Agradecemos pelo seu registro."
            )

            audio_bytes = generate_audio_as_bytes(response_message)
            media_key = upload_file_to_s3(audio_bytes, "audio")
            response_message += f"Para ouvir a resposta em áudio clique no link : " \
            f"https://{self.bucket_name}.s3.amazonaws.com/{media_key}"


        except Exception as e:
            print(e)
            response_message = """Ocorreu um erro ao cadastrar a sua
            instituição. Tente novamente mais tarde."""

        response = LexResponses.sent_fulfillment_response(
            self.event, slots, response_message
        )
        print(f"Response : {response}")
        return response

    def generate_institution_data(self, slots: dict) -> dict:
        """
        Method responsible for generating the dictionary with the institution's
        data from the slot values.
        """
        slot_names = [slot_name for slot_name in slots.keys()]
        slot_values = {name: get_slot_value(slots, name) for name in slot_names}

        institution_data = {
            "cnpj": slot_values["CNPJ"],
            "name": slot_values["InstitutionName"],
            "email": slot_values["InstitutionEmail"],
            "phone_number": slot_values["InstitutionPhone"],
            "region": slot_values["InstitutionRegion"],
            "state": slot_values["InstitutionState"],
            "address": slot_values["InstitutionAddress"],
            "city": slot_values["InstitutionCity"],
            "neighborhood": slot_values["InstitutionNeighborhood"],
            "cep": slot_values["InstitutionCep"],
            "address_number": slot_values["InstitutionAddressNumber"],
            "confirmation_audio": "https://www.teste.com.br",
            "image": f"https://{self.bucket_name}.s3.amazonaws.com/{slot_values["ImagePath"]}",
            "about": slot_values["InstitutionDescription"],
            "site": slot_values["InstitutionSite"],
        }

        return institution_data
