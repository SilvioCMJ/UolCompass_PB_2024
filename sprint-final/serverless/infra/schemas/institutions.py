from typing import Optional
from pydantic import Field
from infra.schemas.base import BaseSchema


url_pattern = r"^(http|https):\/\/[^\s$.?#].[^\s]*$"
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class CreateInstitution(BaseSchema):
    """Schema for creating a new institution"""

    cnpj: str = Field(
        max_length=14,
        description="CNPJ of the institution",
        examples=["12345678000195"],
    )
    name: str = Field(
        description="Name of the institution", examples=["Doação Solidária"]
    )
    email: str = Field(
        pattern=email_pattern,
        description="Contact email of the institution",
        examples=["conexaosolidaria@gmail.com"],
    )
    phone_number: str = Field(
        max_length=11,
        description="Phone number of the institution with area code",
        examples=["11987654321"],
    )
    region: str = Field(
        description="Region where the institution is located", examples=["Norte, Sul"]
    )
    state: str = Field(
        description="State abbreviation where the institution is located",
        examples=["CA"],
    )
    cep: str = Field(
        max_length=8,
        description="Postal code (CEP) of the institution's address",
        examples=["12345678"],
    )
    address: str = Field(
        description="The street address, street name and number if applicable.",
        examples=["Rua das Flores, 123", "Avenida Paulista, 1500"],
    )
    address_number: int = Field(
        description="Number of the address where the institution is located",
        examples=[100],
    )
    city: str = Field(
        description="The city where the address is located.",
        examples=["São Paulo", "Rio de Janeiro"],
    )
    neighborhood: str = Field(
        description="The neighborhood or district within the city.",
        examples=["Centro", "Copacabana"],
    )
    confirmation_audio: str = Field(
        pattern=url_pattern,
        description="URL of the confirmation audio file",
        examples=["https://bucket.s3.us-east-1.amazonaws.com/audio.mp3"],
    )
    image: str = Field(
        pattern=url_pattern,
        description="URL of the institution's image",
        examples=["https://bucket.s3.us-east-1.amazonaws.com/image.jpg"],
    )
    about: str = Field(
        description="Brief description about the institution",
        examples=["Somos emepenhados em espalhar o espírito da bondade e..."],
    )
    site: Optional[str] = Field(
        default=None,
        pattern=url_pattern,
        description="Website URL of the institution",
        examples=["https://institution.com"],
    )


class UpdateInstitution(BaseSchema):
    """Schema for updating an existing institution"""

    cnpj: Optional[str] = Field(
        default=None,
        max_length=14,
        description="Updated CNPJ of the institution",
        examples=["12345678000195"],
    )
    name: Optional[str] = Field(
        default=None,
        description="Updated name of the institution",
        examples=["Coração Solidário"],
    )
    email: Optional[str] = Field(
        pattern=email_pattern,
        default=None,
        description="Updated contact email of the institution",
        examples=["coracaosolidario@gmail.com"],
    )
    phone_number: Optional[str] = Field(
        default=None,
        max_length=11,
        description="Updated phone number of the institution with area code",
        examples=["11987654321"],
    )
    region: Optional[str] = Field(
        default=None,
        description="Updated region of the institution",
        examples=["Nordeste, Oeste"],
    )
    state: Optional[str] = Field(
        default=None,
        description="Updated state abbreviation of the institution",
        examples=["MA"],
    )
    cep: Optional[str] = Field(
        default=None,
        max_length=8,
        description="Updated postal code (CEP) of the institution's address",
        examples=["87654321"],
    )
    address: str = Field(
        default=None,
        description="The street address, street name and number if applicable.",
        examples=["Rua das Flores, 123", "Avenida Paulista, 1500"],
    )
    address_number: Optional[int] = Field(
        default=None,
        description="Updated address number of the institution",
        examples=[250],
    )
    city: str = Field(
        default=None,
        description="The city where the address is located.",
        examples=["São Paulo", "Rio de Janeiro"],
    )
    neighborhood: str = Field(
        default=None,
        description="The neighborhood or district within the city.",
        examples=["Centro", "Copacabana"],
    )
    confirmation_audio: Optional[str] = Field(
        default=None,
        pattern=url_pattern,
        description="Updated URL of the confirmation audio file",
        examples=["https://bucket.s3.us-east-1.amazonaws.com/otheraudio.mp3"],
    )
    image: Optional[str] = Field(
        default=None,
        pattern=url_pattern,
        description="Updated URL of the institution's image",
        examples=["https://bucket.s3.us-east-1.amazonaws.com/otherimage.jpg"],
    )
    about: Optional[str] = Field(
        default=None,
        description="Updated description of the institution",
        examples=["Somos emepenhados em espalhar o espírito da união e..."],
    )
    verified: Optional[bool] = Field(
        default=None,
        description="Verification status of the institution",
        examples=[False],
    )
    site: Optional[str] = Field(
        default=None,
        pattern=url_pattern,
        description="Updated website URL of the institution",
        examples=["https://institution.com"],
    )


class InstitutionResponse(CreateInstitution):
    """Schema to return a single institution"""

    id: str = Field(description="Unique identifier of the institution")
    token: str = Field(description="Authentication token for the institution")
    verified: bool = Field(
        description="Indicates if the institution is verified", examples=[True]
    )


class ListInstitutionReponse(BaseSchema):
    """Schema for returning a list of institutions"""

    institutions: list[InstitutionResponse]
