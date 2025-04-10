import boto3
from botocore.exceptions import ClientError
from core.config import settings


class Bedrock:
    """A class to interact with the Bedrock API for generating suggestions."""

    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=settings.REGION_NAME)

    def _call_bedrock_api(self, message: list) -> dict:
        """Calls the Bedrock API to get a response based on the provided messages."""
        return self.client.converse(
            modelId=settings.MODEL_ID,
            messages=message,
            inferenceConfig={
                "maxTokens": 420,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9,
            },
        )

    def _extract_response_text(self, response: dict) -> str:
        """Extracts the response text from the API response."""

        output = response.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])

        if not content:
            return "No response."

        return content[0].get("text", "No response.")

    def generate_suggestion(self, topic: str) -> dict:
        """Generates a suggestion based on the given topic."""

        # Prepare the message to send to the Bedrock API
        message = [{"role": "user", "content": [{"text": topic}]}]

        try:
            # Call the API and extract the response text
            response = self._call_bedrock_api(message=message)
            response_text = self._extract_response_text(response=response)
        except ClientError as exc:
            # Handle ClientError error from the API call
            print(f"Error obtaining the model's response: {exc}")
            raise

        return {"suggestion": response_text}
