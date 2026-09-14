from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Customer message",
    )


class ChatResponse(BaseModel):
    success: bool
    message: str
    response: str