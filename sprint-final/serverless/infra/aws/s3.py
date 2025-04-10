import boto3
from core.config import settings


class S3:
    """Provides methods to interact with AWS S3 for storing and retrieving objects."""

    def __init__(self) -> None:
        self.client = boto3.client("s3", region_name=settings.REGION_NAME)

    def put_object(self, bucket: str, body: bytes, key: str, contentType: str) -> None:
        """Stores the file in the bucket."""
        self.client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType=contentType
        )

    def get_object(self, bucket: str, key: str) -> bytes:
        """Retrieves the object from S3 and returns its content as bytes."""
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()
