import json
from typing import Any


def build_http_response(
    status_code: int, body: dict, content_type: str = "application/json"
) -> dict[str, Any]:
    """Retorna uma resposta HTTP com status, corpo e cabeçalho."""
    return {
        "statusCode": status_code,
        "body": json.dumps(body, ensure_ascii=False, indent=4),
        "headers": {"Content-Type": content_type},
    }
