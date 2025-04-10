from pydantic import Field
from infra.schemas.base import BaseSchema


class ScanIn(BaseSchema):
    """Input Schema for image scanning."""

    bucket: str = Field(
        description="The S3 bucket where the image is stored.",
        examples=["my-s3-bucket"],
    )
    image_key: str = Field(
        description="The S3 key of the image to be analyzed.",
        examples="images/sample.jpg",
    )


class Label(BaseSchema):
    """Schema representing a label of inappropriate content detected in the image."""

    name: str = Field(description="Name of the label.", examples=["Explicit Nudity"])
    confidence: float = Field(
        description="Confidence score of the label.", examples=[95.5]
    )


class ScanOut(BaseSchema):
    """Output Schema for the result of content scanning."""

    message: str = Field(
        description="Message indicating if inappropriate content was found.",
        examples=["The image contains inappropriate content."],
    )
    labels: list[Label] = Field(
        description="List of inappropriate content labels with confidence scores.",
        examples=[
            {"name": "Explicit Nudity", "confidence": 95.5},
            {"name": "Suggestive", "confidence": 87.3},
        ],
    )
