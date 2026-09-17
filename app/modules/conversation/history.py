from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversation.database_service import (
    get_or_create_conversation,
    get_messages,
)


async def get_conversation_history_from_db(
    db: AsyncSession,
    session_id: str,
    limit: int = 10,
) -> tuple[object, list[dict]]:

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