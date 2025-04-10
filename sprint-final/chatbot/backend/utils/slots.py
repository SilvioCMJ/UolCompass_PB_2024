import re
import os
import requests
from typing import Optional
from utils.responses import LexResponses
from services.api import ApiClient
from services.via_cep_api import ViaCepService


def get_slot_value(slots: str, slot_name: str) -> str:
    """Helper function to safely retrieve the interpreted value of a slot."""

    slot = slots.get(slot_name)
    if slot and "value" in slot:
        return slot["value"].get("interpretedValue")
    return None


def validate_slot(slot_value: str, pattern: str) -> bool:
    """Validates the slot value based on the provided regex pattern."""
    return bool(re.match(pattern, slot_value, re.IGNORECASE))


def update_multiple_slot_values(event: dict, slots_values: dict) -> None:
    """
    Updates multiple slot values in the event with the required format.
    """
    for slot_name, value in slots_values.items():
        event["sessionState"]["intent"]["slots"][slot_name] = {
            "shape": "Scalar",
            "value": {"interpretedValue": value},
        }


def check_image_path_slot(
    slot_value: str, event: dict, slot_name: str
) -> Optional[dict]:
    """Checks if the provided image is appropriate using Amazon Rekognition
    to analyze its content."""

    bucket_name = os.getenv("BUCKET_NAME")

    rekognition_response = requests.post(
        os.getenv("REKOGNITION_ENDPOINT"),
        json={"bucket": bucket_name, "image_key": slot_value},
    )

    print(f"Resposta do Rekognition - Status Code: {rekognition_response.status_code}")

    if rekognition_response.status_code != 204:
        return LexResponses.elicit_slot(event, slot_name)

    return None


def check_slot_filling(slots: dict, event: dict, validation_rules: dict) -> None:
    """
    Responsible for checking if the slots are properly filled.
    """

    intent_name = event["sessionState"]["intent"]["name"]

    for slot_name, slot_data in slots.items():
        slot_value = (
            slot_data.get("value", {}).get("interpretedValue")
            if slot_data and slot_data.get("value")
            else None
        )
        pattern = validation_rules.get(slot_name)

        if pattern and slot_value is not None:
            is_valid = validate_slot(slot_value, pattern)
            if not is_valid:
                return LexResponses.elicit_slot(event, slot_name)

        if slot_name == "ImagePath" and slot_value:
            image_check_response = check_image_path_slot(slot_value, event, slot_name)
            if image_check_response:
                return image_check_response

    print(event)
    if intent_name == "RegisterIntent":
        cep = get_slot_value(slots, "InstitutionCep")

        if cep:
            api_client = ApiClient(os.getenv("BASE_VIA_CEP"))
            via_cep = ViaCepService(api_client)
            address_data = via_cep.get_cep(cep)

            if address_data:
                street, neighborhood, city, state, region = via_cep.format_cep_response(
                    address_data
                )

                slots_values_to_update = {
                    "InstitutionState": state,
                    "InstitutionCity": city,
                    "InstitutionNeighborhood": neighborhood,
                    "InstitutionAddress": street,
                    "InstitutionRegion": region,
                }
                update_multiple_slot_values(event, slots_values_to_update)

                print(event)

                return LexResponses.delegate(event)
            else:
                return LexResponses.elicit_slot(event, "InstitutionCep")

    return LexResponses.delegate(event)
