from pydantic import BaseModel


class ConversationMessage(BaseModel):
    role: str
    content: str


class ConversationHistoryResponse(BaseModel):
    success: bool
    session_id: str
    messages: list[ConversationMessage]