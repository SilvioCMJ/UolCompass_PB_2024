import json
from aws_lambda_powertools.utilities.typing import LambdaContext
from infra.schemas.rekognition import ScanIn, ScanOut
from botocore.exceptions import ClientError
from infra.aws.rekognition import Rekognition
from aws_lambda_powertools.utilities.parser import parse, ValidationError
from utils.build import build_http_response


def scan(event: dict, context: LambdaContext):
    """Analyze an image for inappropriate content."""
    rekognition = Rekognition()

    try:
        # Parse the incoming event body
        data = parse(event=json.loads(event.get("body")), model=ScanIn)
        # Gets the bucket name and image key from the parsed request data
        bucket = data.bucket
        image_key = data.image_key

        # Scans the image using Rekognition
        rekognition_response = rekognition.scan_for_inappropriate_content(
            bucket=bucket, image_key=image_key
        )
    except ValidationError as exc:
        return build_http_response(
            status_code=400, body={"ValidationError": exc.errors(include_url=False)}
        )
    except ClientError as exc:
        return build_http_response(status_code=500, body={"error": str(exc)})

    if not rekognition_response:
        # If there are no inappropriate content labels, nothing will be returned
        return build_http_response(status_code=204, body=rekognition_response)

    scan_response = ScanOut(**rekognition_response)

    return build_http_response(status_code=200, body=scan_response.model_dump())
