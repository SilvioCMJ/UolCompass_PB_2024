import re


def get_twilio_phone_number(params: dict) -> str:
    """Extracts and formats the 'From' number from the parameters."""
    from_number = params.get("From", "")
    numbers = re.findall(r"\d+", from_number)
    formatted_number = "".join(numbers)
    return formatted_number
