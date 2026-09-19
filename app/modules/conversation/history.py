from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversation.database_service import (
    get_messages,
    get_or_create_conversation,
)
from app.modules.conversation.models import Conversation


async def get_conversation_history_from_db(
    db: AsyncSession,
    session_id: str,
    limit: int = 10,
) -> tuple[Conversation, list[dict]]:

    conversation = await get_or_create_conversation(
        db=db,
        session_id=session_id,
    )

    messages = await get_messages(
        db=db,
        conversation=conversation,
        limit=limit,
    )

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    return conversation, history