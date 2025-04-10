import boto3
import uuid
import os

bucket_name = os.getenv("BUCKET_NAME")
s3_client = boto3.client("s3")


def upload_file_to_s3(media_content: bytes, content_type: str) -> str:
    """Uploads the media file content to an S3 bucket and returns the S3 key."""

    extension = (
        ".jpg" if content_type == "image" else ".mp3" if content_type == "audio" else ""
    )

    media_key = f"{uuid.uuid4()}{extension}"

    s3_client.put_object(Bucket=bucket_name, Key=media_key, Body=media_content)

    return media_key
