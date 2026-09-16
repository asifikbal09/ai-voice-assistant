from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        min_length=1,
        description="Conversation session ID",
    )

    message: str = Field(
        ...,
        min_length=1,
        description="Customer message",
    )


class ChatResponse(BaseModel):
    success: bool
    message: str
    response: str