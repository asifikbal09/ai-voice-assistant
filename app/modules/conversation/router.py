from fastapi import APIRouter

from app.modules.conversation.service import (
    get_conversation_history,
    clear_conversation,
)
from app.modules.conversation.shemas import ConversationHistoryResponse

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
)


@router.get(
    "/{session_id}",
    response_model=ConversationHistoryResponse,
)
async def conversation_history(session_id: str):
    messages = get_conversation_history(session_id)

    return {
        "success": True,
        "session_id": session_id,
        "messages": messages,
    }


@router.delete("/{session_id}")
async def delete_conversation(session_id: str):
    return clear_conversation(session_id)