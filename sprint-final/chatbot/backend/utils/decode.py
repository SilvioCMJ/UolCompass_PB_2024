import base64
import urllib.parse


def decode_body(event: dict) -> dict:
    """Decodes the event body and returns a dictionary of parameters."""

    body = event["body"]

    if event["isBase64Encoded"]:
        decoded_body = base64.b64decode(body)
        decoded_body_str = decoded_body.decode("utf-8")
        params = dict(urllib.parse.parse_qsl(decoded_body_str))
    else:
        params = dict(urllib.parse.parse_qsl(body))

    return params
