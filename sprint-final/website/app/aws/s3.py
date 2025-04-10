import boto3
from app.settings import REGION_NAME


class S3:
    """Provides methods to interact with AWS S3 for storing and retrieving objects."""

    def __init__(self) -> str:
        self.client = boto3.client("s3", region_name=REGION_NAME)

    def put_object(self, bucket: str, body: bytes, key: str, contentType: str) -> None:
        """Stores the file in the bucket."""
        self.client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType=contentType
        )
        return f"https://{bucket}.s3.{REGION_NAME}.amazonaws.com/{key}"


s3 = S3()
