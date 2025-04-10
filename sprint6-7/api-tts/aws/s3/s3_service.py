import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

def upload_to_s3(file_path: str, text: str, hashcode: str):
    """Envia um arquivo para o bucket S3."""

    s3 = boto3.client('s3')
    bucket_name = os.environ["BUCKET_NAME"]
    audio_s3_dir = os.environ["AUDIO_S3_DIR"]
    filename = f"{text[:10].replace(' ', '_')}_{hashcode}.mp3"
    try:
        with open(file_path, "rb") as file:
            s3.upload_fileobj(file, bucket_name, f"{audio_s3_dir}/{filename}")
        return f"https://{bucket_name}.s3.amazonaws.com/{audio_s3_dir}/{filename}"
    except (BotoCoreError, ClientError) as e:
        print(f"Error uploading to S3: {e}")
        return None
