import boto3
from typing import Any
from botocore.exceptions import ClientError
from app.settings import REGION_NAME, BOT_ID, LOCALE_ID, ALIAS_ID


class DialogFlow:
    """Class for interacting with Amazon Lex."""

    def __init__(self) -> None:
        self.client = boto3.client("lexv2-runtime", region_name=REGION_NAME)

    def post_message(self, message: str, session_id: str) -> dict[str, Any]:
        """Sends a message to Amazon Lex and receives the response."""
        print(message)

        try:
            # Send message or media URL to Lex
            lex_input = {
                "botId": BOT_ID,
                "botAliasId": ALIAS_ID,
                "localeId": LOCALE_ID,
                "sessionId": session_id,
                "text": message,
            }

            response = self.client.recognize_text(**lex_input)
            messages = response.get("messages", [])

        except ClientError as exc:
            return {"error": str(exc), "user": message}

        return {"lex": messages, "user": message}


Chat = DialogFlow()
