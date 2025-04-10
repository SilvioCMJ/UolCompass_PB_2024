from pydantic import Field
from infra.schemas.base import BaseSchema


class SuggestionIn(BaseSchema):
    """Input model for generating suggestions based on a specified topic."""

    topic: str = Field(
        description="The topic for which the suggestion should be generated.",
        example="Artificial Intelligence",
    )


class SuggestionOut(BaseSchema):
    """Output model for the generated suggestion response."""

    suggestion: str = Field(
        description="The suggestion generated based on the provided topic.",
        example="Consider exploring the latest advancements in neural networks.",
    )
