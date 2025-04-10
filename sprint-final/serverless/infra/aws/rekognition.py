import boto3
from core.config import settings
from botocore.exceptions import ClientError


class Rekognition:
    def __init__(self) -> None:
        self.client = boto3.client("rekognition", region_name=settings.REGION_NAME)

    def detect_inappropriate_content_labels(
        self, bucket: str, image_key: str, min_confidence: int = 75
    ) -> dict:
        """
        Identifies labels indicating inappropriate content in an image stored in S3.
        """
        try:
            response = self.client.detect_moderation_labels(
                Image={"S3Object": {"Bucket": bucket, "Name": image_key}},
                MinConfidence=min_confidence,
            )
            return response.get("ModerationLabels", [])
        except ClientError as exc:
            # Handle ClientError error from the API call
            print(f"Error obtaining the detect moderation labels's response: {exc}")
            raise

    def scan_for_inappropriate_content(self, bucket: str, image_key: str) -> dict:
        """Analyzes an image for inappropriate content based on moderation labels."""
        labels = self.detect_inappropriate_content_labels(bucket, image_key)

        if not labels:
            return {}

        # Returns a message and the inappropriate content labels found
        return {
            "message": "The image contains inappropriate content.",
            "labels": [
                {"name": label["Name"], "confidence": label["Confidence"]}
                for label in labels
            ],
        }
