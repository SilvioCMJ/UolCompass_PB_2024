from utils.build import build_http_response


def health(event, context):
    return build_http_response(
        status_code=200,
        body={
            "message": "Go Serverless v4.0!",
        },
    )
