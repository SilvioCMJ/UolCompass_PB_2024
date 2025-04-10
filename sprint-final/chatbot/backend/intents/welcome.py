from utils.responses import LexResponses
from utils.slots import check_slot_filling


class WelcomeIntent:
    """Class responsible for processing the WelcomeIntent"""

    validation_rules = {"FilterBoolean": r"^(sim|não)$", "AvailableIntents": r"^[1-3]$"}

    def __init__(self, event: dict) -> None:
        self.event = event

    def process_dialog_hook(self) -> LexResponses:
        """
        Responsible for processing the DialogCodeHook step of the WelcomeIntent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        return check_slot_filling(slots, self.event, self.__class__.validation_rules)

    def process_full_fillment(self) -> LexResponses:
        """
        Responsible for processing the FulfillmentCodeHook step of the RegisterIntent.
        """
        return LexResponses.delegate(self.event)
