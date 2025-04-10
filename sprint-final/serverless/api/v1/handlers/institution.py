import json
from typing import Any
from core.exceptions import (
    InstitutionAlreadyExistsException,
    InstitutionNotFoundException,
)
from domain.services.institution import InstitutionService
from infra.schemas.institutions import CreateInstitution, UpdateInstitution
from aws_lambda_powertools.utilities.parser import parse, ValidationError
from aws_lambda_powertools.utilities.typing import LambdaContext
from utils.build import build_http_response


def create(event: dict, context: LambdaContext) -> dict[str, Any]:
    """Registers a new Institution in Dynamo."""
    try:
        # Validates the body by parsing to CreateInstitution
        data = parse(event=json.loads(event.get("body")), model=CreateInstitution)
    except ValidationError as exc:
        return build_http_response(
            status_code=400, body={"ValidationError": exc.errors(include_url=False)}
        )
    try:
        institution = InstitutionService.create(data=data)
    except InstitutionAlreadyExistsException as exc:
        return build_http_response(status_code=409, body={"detail": exc.message})

    return build_http_response(status_code=201, body=institution)


def list_items(event: dict, context: LambdaContext) -> list[dict[str, Any]]:
    """Retrieves all Institution records from Dynamo."""
    try:
        institutions = InstitutionService.get_all()
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=500, body={"detail": exc.message})

    return build_http_response(status_code=200, body=institutions)


def retrieve(event: dict, context: LambdaContext) -> dict[str, Any]:
    """Retrieves a specific record using 'cnpj' as a filter."""

    # Retrieves 'cnpj' from the URL
    cnpj = event["pathParameters"]["cnpj"]

    try:
        institution = InstitutionService.get(cnpj=cnpj)
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=404, body={"detail": exc.message})

    return build_http_response(status_code=200, body=institution)


def query(event: dict, context: LambdaContext) -> dict[str, Any]:
    """Queries institutions by optional 'region' and/or 'state' parameters."""
    query_params = event.get("queryStringParameters") or {}
    region = query_params.get("region")
    state = query_params.get("state")

    try:
        institutions = InstitutionService.query(region=region, state=state)
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=404, body={"detail": exc.message})

    return build_http_response(status_code=200, body=institutions)


def update(event: dict, context: LambdaContext) -> dict[str, Any]:
    """Updates the specified fields of a record in Dynamo."""

    # Retrieves 'cnpj' from the URL
    cnpj = event["pathParameters"]["cnpj"]

    try:
        # Validates the body by parsing to UpdateInstitution
        data = parse(event=json.loads(event.get("body")), model=UpdateInstitution)
    except ValidationError as exc:
        return build_http_response(
            status_code=400, body={"ValidationError": exc.errors(include_url=False)}
        )
    try:
        institution = InstitutionService.update(cnpj=cnpj, data=data)
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=404, body={"detail": exc.message})

    return build_http_response(status_code=200, body=institution)


def delete(event: dict, context: LambdaContext) -> bool:
    """Deletes the specific record using 'cnpj' as a filter."""

    # Retrieves 'cnpj' from the URL
    cnpj = event["pathParameters"]["cnpj"]

    try:
        InstitutionService.delete(cnpj=cnpj)
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=404, body={"detail": exc.message})

    return build_http_response(status_code=204, body={})
