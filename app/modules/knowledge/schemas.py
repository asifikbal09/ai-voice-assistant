from pydantic import BaseModel, Field


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Knowledge search query",
    )

    k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of results",
    )