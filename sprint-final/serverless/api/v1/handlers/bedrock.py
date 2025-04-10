import json
from aws_lambda_powertools.utilities.typing import LambdaContext
from infra.aws.bedrock import Bedrock
from infra.schemas.bedrock import SuggestionIn, SuggestionOut
from botocore.exceptions import ClientError
from aws_lambda_powertools.utilities.parser import parse, ValidationError
from utils.build import build_http_response


def suggestions(event: dict, context: LambdaContext):
    """
    Handle suggestions request by processing the input and generating a suggestion.
    """
    bedrock = Bedrock()

    try:
        # Parse the incoming event body
        data = parse(event=json.loads(event.get("body")), model=SuggestionIn)
        # Gets the topic from the parsed request data
        topic = data.topic

        # Generate suggestion using Bedrock
        bedrock_response = bedrock.generate_suggestion(topic=topic)

    except ValidationError as exc:
        return build_http_response(
            status_code=400, body={"ValidationError": exc.errors(include_url=False)}
        )
    except ClientError as exc:
        return build_http_response(status_code=500, body={"error": str(exc)})

    suggestion = SuggestionOut(**bedrock_response)

    return build_http_response(status_code=200, body=suggestion.model_dump())
