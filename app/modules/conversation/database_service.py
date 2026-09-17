from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversation.message_model import ConversationMessage
from app.modules.conversation.models import Conversation


async def get_or_create_conversation(
    db: AsyncSession,
    session_id: str,
) -> Conversation:
    result = await db.execute(
        select(Conversation).where(
            Conversation.session_id == session_id
        )
    )

    conversation = result.scalar_one_or_none()

    if conversation:
        return conversation

    conversation = Conversation(
        session_id=session_id,
    )

    db.add(conversation)

    await db.commit()
    await db.refresh(conversation)

    return conversation


async def save_message(
    db: AsyncSession,
    conversation: Conversation,
    role: str,
    content: str,
) -> ConversationMessage:

    message = ConversationMessage(
        conversation_id=conversation.id,
        role=role,
        content=content,
    )

    db.add(message)

    await db.commit()
    await db.refresh(message)

    return message


async def get_messages(
    db: AsyncSession,
    conversation: Conversation,
    limit: int = 10,
) -> list[ConversationMessage]:

    result = await db.execute(
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id == conversation.id
        )
        .order_by(
            ConversationMessage.created_at.desc()
        )
        .limit(limit)
    )

    messages = list(result.scalars().all())

    messages.reverse()

    return messages