from pynamodb.exceptions import DoesNotExist
from core.exceptions import (
    InstitutionAlreadyExistsException,
    InstitutionNotFoundException,
)
from infra.models.institutions import InstitutionModel
from infra.schemas.institutions import (
    CreateInstitution,
    InstitutionResponse,
    UpdateInstitution,
    ListInstitutionReponse,
)
from typing import Optional
from uuid import uuid4


class InstitutionService:
    """
    Service class to handle institution operations:
    create, get, retrieve, update, delete.
    """

    @staticmethod
    def create(data: CreateInstitution) -> InstitutionResponse:
        """Creates a new institution record."""
        try:
            InstitutionModel.get(hash_key=data.cnpj)
            raise InstitutionAlreadyExistsException(
                message=f"Institution with cnpj '{data.cnpj}' already exists."
            )
        except DoesNotExist:
            # The institution does not exist, proceed with creation
            pass

        # Creates the institution record in DynamoDB
        institution = InstitutionModel(
            cnpj=data.cnpj,
            id=str(uuid4()),  # Generates a new UUID
            token=str(uuid4()),  # Generates a new token
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            cep=data.cep,
            region=data.region,
            state=data.state,
            address=data.address,
            address_number=data.address_number,
            city=data.city,
            neighborhood=data.neighborhood,
            confirmation_audio=data.confirmation_audio,
            image=data.image,
            about=data.about,
            verified=False,
            site=data.site,
        )
        institution.save()

        institution_out = InstitutionResponse(**institution.attribute_values)
        return institution_out.model_dump()

    @staticmethod
    def get_all() -> ListInstitutionReponse:
        """Retrieves all institution records from the database."""
        institutions = list(InstitutionModel.scan())

        if not institutions:
            raise InstitutionNotFoundException(message="No institutions found.")
        institutions_out = [
            InstitutionResponse(**institution.attribute_values).model_dump()
            for institution in institutions
        ]
        return ListInstitutionReponse(institutions=institutions_out).model_dump()

    @staticmethod
    def get(cnpj: str) -> InstitutionResponse:
        """Retrieves a specific institution by its cnpj."""
        try:
            institution = InstitutionModel.get(hash_key=cnpj)
        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )

        institution_out = InstitutionResponse(**institution.attribute_values)
        return institution_out.model_dump()

    @staticmethod
    def query(
        region: Optional[str] = None, state: Optional[str] = None
    ) -> ListInstitutionReponse:
        """Retrieve institutions by region and/or state parameters."""
        if state and region:
            query = InstitutionModel.scan(
                (InstitutionModel.state == state) & (InstitutionModel.region == region)
            )
        elif state:
            query = InstitutionModel.scan(InstitutionModel.state == state)
        elif region:
            query = InstitutionModel.scan(InstitutionModel.region == region)

        institutions = [
            InstitutionResponse(**item.attribute_values).model_dump() for item in query
        ]
        if not institutions:
            raise InstitutionNotFoundException(
                message="No institutions found matching the specified criteria."
            )
        return ListInstitutionReponse(institutions=institutions).model_dump()

    @staticmethod
    def update(cnpj: str, data: UpdateInstitution) -> InstitutionResponse:
        """Updates an existing institution record by its cnpj."""
        try:
            institution = InstitutionModel.get(hash_key=cnpj)

            # update actions
            updates = [
                getattr(InstitutionModel, field).set(value)
                for field, value in data.model_dump(exclude_unset=True).items()
            ]
            institution.update(actions=updates)

        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )
        institution_out = InstitutionResponse(**institution.attribute_values)
        return institution_out.model_dump()

    @staticmethod
    def delete(cnpj: str) -> bool:
        """Deletes an institution by its cnpj."""
        try:
            institution = InstitutionModel.get(hash_key=cnpj)
        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )

        institution.delete()
        return True
