from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversation.message_model import ConversationMessage
from app.modules.conversation.models import Conversation

ALLOWED_ROLES = {"user", "assistant"}


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

    try:
        await db.commit()
        await db.refresh(conversation)

    except Exception:
        await db.rollback()
        raise

    return conversation


async def save_message(
    db: AsyncSession,
    conversation: Conversation,
    role: str,
    content: str,
) -> ConversationMessage:

    if role not in ALLOWED_ROLES:
        raise ValueError(
            f"Invalid message role: {role}"
        )

    if not content or not content.strip():
        raise ValueError(
            "Message content cannot be empty."
        )

    message = ConversationMessage(
        conversation_id=conversation.id,
        role=role,
        content=content.strip(),
    )

    db.add(message)

    # Explicitly update conversation timestamp.
    conversation.updated_at = func.now()

    try:
        await db.commit()
        await db.refresh(message)

    except Exception:
        await db.rollback()
        raise

    return message


async def get_messages(
    db: AsyncSession,
    conversation: Conversation,
    limit: int = 10,
) -> list[ConversationMessage]:

    if limit < 1:
        limit = 10

    result = await db.execute(
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id
            == conversation.id
        )
        .order_by(
            ConversationMessage.created_at.desc()
        )
        .limit(limit)
    )

    messages = list(result.scalars().all())

    messages.reverse()

    return messages

async def save_message_pair(
    db: AsyncSession,
    conversation: Conversation,
    user_content: str,
    assistant_content: str,
) -> tuple[ConversationMessage, ConversationMessage]:

    if not user_content.strip():
        raise ValueError(
            "User message cannot be empty."
        )

    if not assistant_content.strip():
        raise ValueError(
            "Assistant message cannot be empty."
        )

    user_message = ConversationMessage(
        conversation_id=conversation.id,
        role="user",
        content=user_content.strip(),
    )

    assistant_message = ConversationMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_content.strip(),
    )

    db.add(user_message)
    db.add(assistant_message)

    conversation.updated_at = func.now()

    try:
        await db.commit()

        await db.refresh(user_message)
        await db.refresh(assistant_message)

    except Exception:
        await db.rollback()
        raise

    return user_message, assistant_message