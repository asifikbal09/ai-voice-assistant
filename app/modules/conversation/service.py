from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversation.database_service import (
    get_messages,
    get_or_create_conversation,
)
from app.modules.conversation.memory import conversation_memory


async def get_conversation_history(
    db: AsyncSession,
    session_id: str,
):

    conversation = await get_or_create_conversation(
        db=db,
        session_id=session_id,
    )

    messages = await get_messages(
        db=db,
        conversation=conversation,
        limit=100,
    )

    return messages


def clear_conversation(session_id: str):
    conversation_memory.clear_session(session_id)

    return {
        "success": True,
        "session_id": session_id,
        "message": "Conversation cleared successfully.",
    }