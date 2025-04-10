class LexResponses:
    """
    A class to format responses for Amazon Lex.
    """

    MAX_ATTEMPTS = 3

    @staticmethod
    def sent_fulfillment_response(
        event: dict, slots: dict, response_message: str
    ) -> dict:
        """
        Sends a response to Amazon Lex when all slots are fulfilled.
        """

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Fulfilled",
                    "slots": slots,
                },
            },
            "messages": [{"contentType": "PlainText", "content": response_message}],
        }

    @staticmethod
    def elicit_slot(event, slot_to_elicit):
        """
        Sends a response to Amazon Lex to request a specific slot from the user.
        """
        session_attributes = event.get("sessionState", {}).get("sessionAttributes", {})
        attempt_key = f"{slot_to_elicit}_attempts"
        continue_key = "continue_prompt"

        if session_attributes.get(continue_key) == "waiting_for_confirmation":
            user_response = event.get("inputTranscript", "").strip().lower()

            if user_response == "encerrar":
                return {
                    "sessionState": {
                        "dialogAction": {"type": "Close"},
                        "intent": {
                            "name": event["sessionState"]["intent"]["name"],
                            "state": "Fulfilled",
                        },
                        "sessionAttributes": session_attributes,
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": (
                                "Entendido! Se precisar de alguma coisa é só chamar."
                            ),
                        }
                    ],
                }

            elif user_response == "continuar":
                session_attributes[attempt_key] = "0"
                session_attributes.pop(continue_key, None)
                return LexResponses.elicit_slot_response(
                    slot_to_elicit, event, session_attributes
                )

            else:
                return LexResponses.elicit_slot_response(
                    slot_to_elicit,
                    event,
                    session_attributes,
                    "Por favor, responda com 'encerrar' para encerrar ou 'continuar'"
                    "para continuar tentando.",
                )

        attempts = int(session_attributes.get(attempt_key, 0)) + 1
        session_attributes[attempt_key] = str(attempts)

        if attempts >= LexResponses.MAX_ATTEMPTS:
            session_attributes[continue_key] = "waiting_for_confirmation"
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": slot_to_elicit,
                    },
                    "intent": event["sessionState"]["intent"],
                    "sessionAttributes": session_attributes,
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": (
                            "Parece que você está tendo um pouco de dificuldade com "
                            "essa informação.\n"
                            "Deseja encerrar por agora? Responda 'encerrar'"
                            "para encerrar ou 'continuar' para tentar novamente."
                        ),
                    }
                ],
            }

        return LexResponses.elicit_slot_response(
            slot_to_elicit, event, session_attributes
        )

    @staticmethod
    def elicit_slot_response(
        slot_to_elicit, event, session_attributes, message_content=None
    ):
        """
        Helper function to format a response for eliciting a slot with a custom message.
        """
        response = {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": slot_to_elicit},
                "intent": event["sessionState"]["intent"],
                "sessionAttributes": session_attributes,
            }
        }

        if message_content:
            response["messages"] = [
                {"contentType": "PlainText", "content": message_content}
            ]

        return response

    @staticmethod
    def delegate(event):
        """
        Sends a response to Amazon Lex to delegate the conversation.
        """
        return {
            "sessionState": {
                "dialogAction": {"type": "Delegate"},
                "intent": event["sessionState"]["intent"],
            }
        }
